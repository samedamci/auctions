#!/usr/bin/env python3

from flask import render_template, url_for, flash, redirect
from auctions.forms import Register, Login
from auctions.models import User, Auction
from auctions import app, db, bcrypt


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = Login()
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = Register()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(
            f'Account "{form.username.data}" has been created successfully!', "success"
        )
        return redirect(url_for("login"))
    return render_template("register.html", form=form)
