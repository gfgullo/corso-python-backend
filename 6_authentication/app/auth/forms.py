from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from app.models import User


class SignupForm(FlaskForm):
    email = StringField('Your email', validators=[DataRequired(), Email()])
    username = StringField('Your username', validators=[DataRequired()])
    password = PasswordField('Your password', validators=[DataRequired(), EqualTo('confirm_password', "Password must match")])
    confirm_password = PasswordField('Confirm password')
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    email = StringField('Your email', validators=[DataRequired(), Email()])
    password = PasswordField('Your password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')