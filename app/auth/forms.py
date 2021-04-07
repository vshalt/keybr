from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import (
    DataRequired,
    Regexp,
    Email,
    EqualTo,
    Length,
    ValidationError
)
from app.models import User


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=4, max=20),
            Regexp(
                regex="^[a-zA-Z_.][a-zA-Z0-9_.]*$",
                flags=0,
                message=(
                    "Username must contain alphanumericals only.\
                    Username cannot start with numbers"
                ),
            ),
        ],
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("confirm_password", message="Passwords must match"),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired()]
    )
    submit = SubmitField("Register")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already exists')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    new_password = PasswordField(
        'New password',
        validators=[
            DataRequired(),
            EqualTo('confirm_password', message="Password must match")
        ]
    )
    confirm_password = PasswordField(
        'Confirm password', validators=[DataRequired()]
    )
    submit = SubmitField('Change')


class RequestForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send confirmation link')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first() is None:
            raise ValidationError('Email does not exist')

class NewPasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            EqualTo('confirm_password', message="Password must match")
        ],
    )
    confirm_password = PasswordField(
        'Confirm password', validators=[DataRequired()]
    )
    submit = SubmitField('Confirm')

class ChangeEmailForm(FlaskForm):
    old_email = StringField('Old email', validators=[DataRequired(), Email()])
    new_email = StringField('New email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Change')

    def validate_old_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first() is None:
            raise ValidationError('Check email')

    def validate_new_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already in use')

