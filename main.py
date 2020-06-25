#!/usr/bin/env python3

from flask import Flask, render_template, url_for

from settings import SECRET_KEY
from forms import Register, Login

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login")
def login():
    return render_template("login.html", form=Login())


@app.route("/register")
def register():
    return render_template("register.html", form=Register())
