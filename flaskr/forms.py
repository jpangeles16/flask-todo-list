from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskr.models import User

class RegistrationForm(FlaskForm):
    """A registration form where
       a user types in his or her
       desired username, an email, and
       then a password with a confirm password.
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password',  validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up!')

    def validate_username(self, username):
        """ If there is a user that exists with USERNAME in our database, then
            we will raise a validation error.
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken.  Please choose a different one')

    def validate_email(self, email):
        """ If there is an email that exists with EMAIL in our database, then
            we will raise a validation error.
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken.  Please choose a different one')

class LoginForm(FlaskForm):
    """A login form where
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password',  validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')