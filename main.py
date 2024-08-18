from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

import models
from models import db
import crud

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)

with app.app_context():
    db.create_all()


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

        new_user = models.User(name=name, email=email, password=password)
        # Add user through CRUD function
        try:
            crud.add_user(new_user)
            flash('User registered successfully!', 'success')
            return redirect(url_for('secrets', user_id=new_user.id))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
            return redirect(url_for('register'))

    # If it's a GET request, just render the registration form
    return render_template("register.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/secrets')
def secrets():
    user_id = request.args.get('user_id')  # Get user_id from query parameters
    user = crud.get_user_by_id(user_id)
    return render_template("secrets.html", user=user)



@app.route('/logout')
def logout():
    pass


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
