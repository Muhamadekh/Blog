from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from blog.models import User, Post


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20, min=2)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password= PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


    def validate_username (self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The username is already taken. Please choose another username')


    def validate_email (self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email is already taken. Please choose another email')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    remember = BooleanField('Remember Me')


class AccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20, min=2)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Photo', validators=[FileAllowed(['jpeg', 'png'])])
    submit = SubmitField('Update Details')

    def validate_username (self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('The username is already taken. Please choose another username')


    def validate_email (self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('The email is already taken. Please choose another email')

