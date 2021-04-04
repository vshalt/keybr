from flask import (
    render_template, abort, redirect, url_for, current_app, request )
from flask_login import login_required, current_user
from random import shuffle
from app import db
from app.main import main_blueprint
from app.main.forms import EditProfileForm
from app.models import User
from words import words


@main_blueprint.route("/")
def home():
    return render_template("main/home.html")


@main_blueprint.route("/about")
def about():
    return render_template("main/about.html")


@main_blueprint.route("/profile/<username>")
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template("main/profile.html", user=user)


@main_blueprint.route("/edit/<username>")
@login_required
def edit_profile(username):
    if current_user.username != username:
        abort(403)
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    form = EditProfileForm()
    if form.validate_on_submit():
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("main.profile", username=user.username))
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template("main/edit-profile.html", user=user, form=form)


# TODO: logic
@main_blueprint.route("/race")
def race():
    if current_user.is_anonymous:
        user = None
    else:
        user = current_user
    shuffle(words)
    if user:
        user.set_league()
    return render_template("main/race.html", user=user, words=words)


# TODO: logic
@main_blueprint.route("/leaderboard")
def leaderboard():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.points.desc())\
        .paginate(
            page, per_page=current_app.config['PER_PAGE'], error_out=False
        )
    users = pagination.items
    return render_template(
        "main/leaderboard.html", users=users, pagination=pagination
    )
