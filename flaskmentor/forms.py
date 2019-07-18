from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flaskmentor.models import User6
from flask_login import current_user

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Username*"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email*"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password*"})
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm Password*"})
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User6.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The username already exists. Please choose a different one.')

    def validate_email(self, email):
        user = User6.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email*"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password*"})
    #  Secure cookie to let user stay logged in
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class SettingsForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    mentorskills = StringField('Mentor Skills Required', validators=[DataRequired()],
                              render_kw={"placeholder": "Mentor Skills Required (e.g. Python, Java)*"})
    preference = SelectField('Preferred Method of Mentorship',
                             choices=[('Online', 'Online'), ('In Person', 'In Person'),
                                      ('Via Email', 'Via Email'), ('Phone Call', 'Phone Call')],
                             validators=[DataRequired()], render_kw={"placeholder": "Preferred Method of Mentorship*"})
    location = StringField('Location', validators=[DataRequired()], render_kw={"placeholder": "Your Location*"})
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User6.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('The username already exists. Please choose a different one.')

    # def validate_email(self, email):
    #     if email.data != current_user.email:
    #         user = User6.query.filter_by(email=email.data).first()
    #         if user:
    #             raise ValidationError('The email already exists. Please choose a different one.')


def three_skills(form, field):
    message = 'Please provide comma separated 3 skills'
    l = field.data
    arr = l.split(",")  # arr will be a list
    if len(arr) < 3:
        raise ValidationError(message)


class DetailsForm(FlaskForm):
    # skills = StringField('Skills', validators=[DataRequired(), three_skills])
    looking_for = StringField('Mentor Skills Required', validators=[DataRequired()], render_kw={"placeholder": "Mentor Skills Required (e.g. Python, Java)*"})
    #  looking_for can also be made a drop down

    preference = SelectField('Preferred Method of Mentorship', choices = [('Online', 'Online'),  ('In Person', 'In Person'),
                                                                          ('Via Email', 'Via Email'),  ('Phone Call', 'Phone Call')],
                             validators=[DataRequired()], render_kw={"placeholder": "Preferred Method of Mentorship*"})
    location = StringField('Location', validators=[DataRequired()], render_kw={"placeholder": "Your Location*"})
    # location = StringField('Location', [Optional()])
    submit = SubmitField('Search')
