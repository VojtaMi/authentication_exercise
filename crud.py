from models import db, User


def add_user(user):
    # Assuming `user` is an instance of the User model
    db.session.add(user)
    db.session.commit()

def get_user_by_id(user_id):
    return User.query.get_or_404(user_id)
