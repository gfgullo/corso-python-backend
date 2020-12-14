from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class SignupForm(FlaskForm):
    email = StringField('Your email', validators=[DataRequired(), Email()])
    username = StringField('Your username', validators=[DataRequired()])
    password = PasswordField('Your password', validators=[DataRequired(), EqualTo('confirm_password', "Password must match")])
    confirm_password = PasswordField('Confirm password')
    submit = SubmitField('Sign up')