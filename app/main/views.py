from flask import render_template
from app.main import main_blueprint
from app.models import User


@main_blueprint.route("/")
def home():
    return render_template("main/home.html")


@main_blueprint.route("/about")
def about():
    return render_template("main/about.html")


@main_blueprint.route("/profile/<username>")
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("main/profile.html", user=user)


@main_blueprint.route("/race")
def race():
    return render_template("main/race.html")


@main_blueprint.route("/leaderboard")
def leaderboard():
    return render_template("main/leaderboard.html")
