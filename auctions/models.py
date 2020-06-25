#!/usr/bin/env python3

from datetime import datetime
from auctions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(22), unique=True, nullable=False)
    email = db.Column(db.String(122), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    auctions = db.relationship("Auction", backref="seller", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_end = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    buy_now_price = db.Column(db.Float)
    call_price = db.Column(db.Float)
    image = db.Column(db.String(20), nullable=False)

    def __repr_(self):
        return f"Auction('{self.title}', '{self.date_posted}')"
