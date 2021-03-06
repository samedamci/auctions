#!/usr/bin/env python3

from flask import render_template, url_for, flash, redirect, jsonify, request
from auctions.forms import Register, Login, AddAuction
from auctions.models import User, Auction
from auctions import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


# Displayed all time.
@app.route("/")
def home():
    return render_template("auctions.html", auction=Auction)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/auction/<id>")
def auction(id):
    auction = Auction.query.get(id)
    return render_template(
        "auction.html",
        title=auction.title,
        description=auction.description,
        call_price=auction.call_price,
        buy_now_price=auction.buy_now_price,
        date_posted=auction.date_posted,
        date_posted_human=str(auction.date_posted).split(".", 1)[0],
        date_end=auction.date_end,
        date_now=datetime.utcnow(),
        image=auction.image,
    )


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
    return render_template("settings.html")


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@app.route("/observed")
@login_required
def observed():
    return render_template("observed.html")


@app.route("/cart")
@login_required
def cart():
    return render_template("cart.html")


@app.route("/add_auction", methods=["GET", "POST"])
@login_required
def add_auction():
    if current_user.is_authenticated:
        form = AddAuction()
        if form.validate_on_submit():
            auction = Auction(
                title=form.title.data,
                description=form.description.data,
                date_end=form.date_end.data,
                buy_now_price=form.buy_now_price.data,
                call_price=form.call_price.data,
                image=form.image.data,
                user_id=User.query.filter_by(username=current_user.username).first().id,
            )
            db.session.add(auction)
            db.session.commit()
            flash(f'Auction "{form.title.data}" has been added!', "success")
            return redirect(url_for("auctions"))
        return render_template("add_auction.html", form=form)


# API.
auction_list = []
auction_count = Auction.query.count()
for id in range(auction_count):
    auction_ = Auction.query.get(id + 1)
    auction_list.append(
        {
            "id": id + 1,
            "title": auction_.title,
            "date_posted": auction_.date_posted,
            "date_end": auction_.date_end,
            "description": auction_.description,
            "buy_now_price": auction_.buy_now_price,
            "call_price": auction_.call_price,
            "image": auction_.image,
            "user_id": auction_.user_id,
        }
    )


@app.route("/api/auctions/all", methods=["GET"])
def api_all():
    return jsonify(auction_list)


@app.route("/api/auctions", methods=["GET"])
def api_id():
    if "id" in request.args:
        id = int(request.args["id"])
        if id > auction_count or id <= 0:
            return "Error: Invalid id.\n"
    else:
        return "Error: No id field provided. Please specify an id.\n"

    results = []
    for auction in auction_list:
        if auction["id"] == id:
            results.append(auction)

    return jsonify(results)
