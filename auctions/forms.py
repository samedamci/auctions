#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    FloatField,
    FileField,
    DateField,
)
# from wtforms.fields.html5 import DateField
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    Optional,
)
from datetime import datetime, timedelta
from auctions.models import User


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

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is taken, choose another.")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Account with this email address exists!")


class Login(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Sign In")


class AddAuction(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=3, max=100)])
    description = StringField("Description", validators=[DataRequired()])
    date_end = DateField(
        "End of auction date",
        default=((datetime.now() + timedelta(days=1))),
        validators=[DataRequired()],
    )
    buy_now_price = FloatField("Buy now price", validators=[Optional()])
    call_price = FloatField("Call price", validators=[DataRequired()])
    image = FileField("Picture", validators=[Optional()])
    submit = SubmitField("Add auction")
