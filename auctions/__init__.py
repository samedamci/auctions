#!/usr/bin/env python3

import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

dotenv_path = join(dirname(__file__), "../.env")
load_dotenv(dotenv_path)
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from auctions import routes
