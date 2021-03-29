from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length


class EditProfileForm(FlaskForm):
    name = StringField("Name", validators=[Length(min=0, max=32)])
    location = StringField("Location", validators=[Length(min=0, max=32)])
    about_me = StringField("About me")
    submit = SubmitField("Submit")
