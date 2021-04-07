from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from app import db, login_manager

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


    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(
            secret_key=current_app.config['SECRET_KEY'], expires_in=expiration
        )
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        else:
            self.is_confirmed = True
            db.session.add(self)
            return True

    def generate_forgot_password_token(self, expiration=3600):
        s = Serializer(
            secret_key=current_app.config['SECRET_KEY'], expires_in=expiration
        )
        return s.dumps({'forgot': self.id}).decode('utf-8')

    def confirm_forgot_password_token(self, token):
        s = Serializer(secret_key=current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('forgot') != self.id:
            return False
        return True

    def generate_change_email_token(self, new_email, expiration=3600):
        s = Serializer(
            secret_key=current_app.config['SECRET_KEY'], expires_in=expiration
        )
        return s.dumps({"id": self.id, "email": new_email}).decode('utf-8')

    def confirm_change_email_token(self, token):
        s = Serializer(secret_key=current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get("id") != self.id:
            return False
        self.email = data.get("email")
        db.session.add(self)
        return True

    def change_password(self, old: str, new: str) -> bool:
        if self.verify_password(old):
            self.password = new
            db.session.add(self)
            return True
        return False

    def change_username(self, new: str) -> None:
        self.username = new
        db.session.add(self)

    def set_league(self):
        if self.points >= 1000:
            self.league = 'Diamond'
        elif self.points >= 800:
            self.league = 'Platinum'
        elif self.points >= 600:
            self.league = 'Gold'
        elif self.points >=400:
            self.league = 'Silver'
        elif self.points >= 100:
            self.league = 'Bronze'
        db.session.add(self)

class AnonymousUser(AnonymousUserMixin):
    pass

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id: int) -> User:
    return User.query.get(int(user_id))
