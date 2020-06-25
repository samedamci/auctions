#!/usr/bin/env python3

from flask import render_template, url_for, flash, redirect
from auctions.forms import Register, Login
from auctions.models import User, Auction
from auctions import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def home():
    return render_template("index.html")


# Displayed all time.
@app.route("/about")
def about():
    return render_template("about.html")


# Displayed if user not logged in.
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("home"))
        else:
            flash("Something goes wrong! Check your login data!", "failed")
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
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


# Displayed if user logged in.
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/settings")
@login_required
def settings():
    return render_template('settings.html')


@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html')


@app.route("/observed")
@login_required
def observed():
    return render_template('observed.html')


@app.route("/cart")
@login_required
def cart():
    return render_template('cart.html')
