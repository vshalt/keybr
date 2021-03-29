from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Regexp, Email, EqualTo, Length


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
                        Username cannot start with '_' or '.'"
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

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
