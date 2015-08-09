from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, \
     ValidationError
from ..models import User

class LoginForm(Form):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Keep me logged in')


class SignupForm(Form):
    username = StringField('Username', 
                validators=[DataRequired(), Length(3, 80),
                Email()])
    password = PasswordField('Password',
                    validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm Password',
                    validators=[DataRequired()])
    name = StringField('Full Name', 
                validators=[DataRequired(), Length(3, 120),
                Regexp('^[A-Za-z ]{3,80}$',
                message='Please enter your full name. The name must be atleast 3 characters long, umbers and special characters are not allowed')])
    submit = SubmitField('Signup')

    def validate_username(self, username_field):
        if User.get_by_username(username_field.data):
            raise ValidationError('This username is already taken.')