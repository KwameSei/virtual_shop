from cProfile import label
import email
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
# Using validators
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User

class RegisterForm(FlaskForm):
    # Checking and validating existing username:
    def validate_username(self, username_check):
        user = User.query.filter_by(username=username_check.data).first()
        if user:    # Throw error if username already exists
            raise ValidationError('Username already exists! Please try a different one')

    # Checking and validating existing email address
    def validate_email_address(self, email_check):
        email = User.query.filter_by(email_address=email_check.data).first()
        if email:
            raise ValidationError('Email already exists in our database! Please use a different one')

    username = StringField(label='User Name', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')
    # Note: Go to the route.py to create an instance of the registration

class LoginForm(FlaskForm):
    username = StringField(label='User Name')
    email_address = StringField(label='Email Address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')
    # Note: Go to the route.py to create an instance of the login