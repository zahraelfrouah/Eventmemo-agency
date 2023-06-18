

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, FileField, DateTimeField, DateTimeLocalField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired, EqualTo, length
from wtforms.widgets import TextArea


class Login(FlaskForm):
      email = StringField('EMAIL', validators=[DataRequired()])
      password = PasswordField('PASSWORD', validators=[DataRequired()])
      submit = SubmitField('Log in with eventmemo')


class EditProfile(FlaskForm):
      username = StringField('USERNAME', validators=[DataRequired()])
      email = StringField('EMAIL', validators=[DataRequired()])
      password = PasswordField('PASSWORD', validators=[DataRequired()])
      profil_pic = FileField('')
      submit = SubmitField('save changes')


class Sign_up(FlaskForm):
      username = StringField('USERNAME', validators=[DataRequired()])
      email = StringField('EMAIL', validators=[DataRequired()])
      password_hash = PasswordField('PASSWORD', validators=[DataRequired(), EqualTo(
                'password_hash2', message='Passwords Must Match')])
      password_hash2 = PasswordField(
                'CONFIRM PASSWORD', validators=[DataRequired()])
      profil_pic = FileField('Profile Pic')
      submit = SubmitField('Create eventmemo account')


class PostForm(FlaskForm):
      title = StringField("Title", validators=[DataRequired()])
      start = DateTimeLocalField(
          "Start", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
      end = DateTimeLocalField("End", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
      slug = StringField("Slug", validators=[DataRequired()])
      place = StringField('location', validators=[DataRequired()])
      image = FileField('Image')
      submit = SubmitField("Upload event")

class EditEventForm(FlaskForm):
      title = StringField('Title', validators=[DataRequired()])
      start = DateTimeLocalField(
          "Start", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
      end = DateTimeLocalField("End", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
      slug = StringField('Slug', validators=[DataRequired()])
      place = StringField('location', validators=[DataRequired()])
      image = FileField('Image')
      submit = SubmitField('Save Changes')

class CommentForm(FlaskForm):
    text = StringField(validators=[
        InputRequired(), Length(min=4, max=26)], render_kw={"placeholder": "comment some"})

    submit = SubmitField('Comment')