#!/usr/bin/env python3

from flask import render_template, url_for, flash, redirect
from auctions.forms import Register, Login
from auctions.models import User, Auction
from auctions import app


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
        flash(f'Account "{form.username.data}" created successfully!', "success")
        return redirect(url_for("home"))
    return render_template("register.html", form=form)
