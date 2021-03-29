from app import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(32), index=True, nullable=False)
    is_confirmed = db.Column(db.Boolean(), default=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(32))
    location = db.Column(db.String(32))
    about_me = db.Column(db.Text())
    league = db.Column(db.String(16), default="unranked")
    points = db.Column(db.Integer, default=0)
    highscore = db.Column(db.Integer(), default=0)
    last_ten_scores = db.Column(db.Text)


class AnonymousUser(AnonymousUserMixin):
    pass


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
