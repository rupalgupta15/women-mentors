from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskmentor.models import User


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Username*"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email*"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password*"})
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm Password*"})
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The username already exists. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email*"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password*"})
    #  Secure cookie to let user stay logged in
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


def three_skills(form, field):
    message = 'Please provide comma separated 3 skills'
    l = field.data
    arr = l.split(",")  # arr will be a list
    if len(arr) < 3:
        raise ValidationError(message)


class DetailsForm(FlaskForm):
    # skills = StringField('Skills', validators=[DataRequired(), three_skills])
    looking_for = StringField('Mentor Skills Required', validators=[DataRequired()], render_kw={"placeholder": "Mentor Skills Required*"})
    #  looking_for can also be made a drop down
    location = StringField('Location', validators=[DataRequired()], render_kw={"placeholder": "Your Location*"})
    preference = SelectField('Preferred Method of Mentorship', choices = [('Online', 'Online'),  ('In Person', 'In Person'),
                                                                          ('Via Email', 'Via Email'),  ('Phone Call', 'Phone Call')],
                             validators=[DataRequired()], render_kw={"placeholder": "Preferred Method of Mentorship*"})
    submit = SubmitField('Search')
