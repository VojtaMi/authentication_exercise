from models import db, User


def add_user(user):
    # Assuming `user` is an instance of the User model
    db.session.add(user)
    db.session.commit()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def email_exists(email):
    return User.query.filter_by(email=email).first() is not None
