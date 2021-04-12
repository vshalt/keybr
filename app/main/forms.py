from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import Length, ValidationError, DataRequired, Regexp
from app.models import User


class SelectDurationForm(FlaskForm):
    time = RadioField(
        'Duration',
        choices=[(1, 'one minute'), (2, 'two minutes')],
        coerce=int,
        default=1
    )
    submit = SubmitField('Start')
    

class EditProfileForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                regex="^[a-zA-Z_.][a-zA-Z_.0-9]*$",
                flags=0,
                message=(
                    "Username must contain alphanumericals only.\
                        Username cannot start with numbers"
                )
            ),
        ]
    )
    name = StringField("Name", validators=[Length(min=0, max=32)])
    location = StringField("Location", validators=[Length(min=0, max=32)])
    about_me = StringField("About me")
    submit = SubmitField("Submit")

    def validate_new_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists')
