from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email

class NewUserForm(FlaskForm):
    """Form for user"""
    username = StringField('Username', validators=[InputRequired(message='Please enter a Username'), Length(min=1, max=20, message='Please select a valid length of between 1 and 20 characters')])
    password = PasswordField('Password', validators=[InputRequired(message='Please enter a password')])
    email = StringField('Email Address', validators=[InputRequired(message='Please enter an email address'), Length(min=6, max=50, message='Please enter a valid length between 6 and 50 characters'), Email(message='Please enter a valid email address')])
    first_name = StringField('First Name', validators=[InputRequired('Please enter a first name'), Length(min=1, max=30, message='Please enter a valid length of between 1 and 30 characters')])
    last_name = StringField('Last Name', validators=[InputRequired('Please enter a last name'), Length(min=1, max=30, message='Please enter a valid length of between 1 and 30 characters')])

class UserLoginForm(FlaskForm):
    """Form for user"""
    username = StringField('Username', validators=[InputRequired(message='Please enter a Username'), Length(min=1, max=20, message='Please select a valid length of between 1 and 20 characters')])
    password = PasswordField('Password', validators=[InputRequired(message='Please enter a password')])

class FeedbackForm(FlaskForm):
    """Form for User Feedback"""
    title = StringField('Title', validators=[InputRequired(message='Please enter a title'), Length(min=1, max=100, message='Please select a valid length between 1 and 100 characters')])
    content = StringField('Content', validators=[InputRequired(message='Please enter content')])
    