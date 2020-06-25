#!/usr/bin/env python3

from flask import Flask, render_template, url_for, flash, redirect

from settings import SECRET_KEY
from forms import Register, Login

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


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
