import os
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import flask_login as fl_log
from flask_login import login_required
import dotenv

import models
from models import db
import crud

dotenv.load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)

login_manager = fl_log.LoginManager()
# redirect user to login page when trying to access a content behind authentication
login_manager.login_view = 'login'  # Redirect to the login page
login_manager.login_message_category = 'danger'  # Flash category for the message

login_manager.init_app(app)

with app.app_context():
    db.create_all()


@app.context_processor
def inject_user():
    return {'current_user': fl_log.current_user}


@login_manager.user_loader
def load_user(user_id):
    return crud.get_user_by_id(user_id)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        password_hash = generate_password_hash(password, "pbkdf2", salt_length=8)

        new_user = models.User(name=name, email=email, password=password_hash)
        # Add user through CRUD function
        try:
            crud.add_user(new_user)
            return redirect(url_for('secrets'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
            return redirect(url_for('register'))

    # If it's a GET request, just render the registration form
    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Use the CRUD function to get the user by email
        user = crud.get_user_by_email(email)

        if not user:
            flash("this email is not registered", "danger")
        elif not check_password_hash(user.password, password):
            flash("password is incorrect", "danger")
        else:
            # Login user
            fl_log.login_user(user)
            return redirect(url_for('secrets'))

    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html", user=fl_log.current_user)


@app.route('/logout')
@login_required
def logout():
    fl_log.logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/download')
def download():
    # Specify the directory relative to your application's root
    directory = 'static/files'
    # Specify the file name
    filename = 'cheat_sheet.pdf'

    # Serve the file for download
    return send_from_directory(directory, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
