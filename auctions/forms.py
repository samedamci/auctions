#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class Register(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=5, max=22)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm password",
        validators=[DataRequired(), Length(min=8, max=128), EqualTo("password")],
    )
    submit = SubmitField("Sign Up")


class Login(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')
