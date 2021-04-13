from flask import (
    render_template, abort, redirect, url_for, current_app, request, flash
)
from flask_login import login_required, current_user
from app import db
from app.main import main_blueprint
from app.main.forms import EditProfileForm, SelectDurationForm
from app.models import User


@main_blueprint.route("/", methods=['POST', 'GET'])
def home():
    form = SelectDurationForm()
    flash(
        'Computer is recommended for this website. Login to get ranked',
        'success'
    )
    if form.validate_on_submit():
        print(form.time.choices[0])
        time = form.time.data
        return redirect(url_for('main.race', time=time))
    return render_template("main/home.html", form=form)


@main_blueprint.route("/about")
def about():
    return render_template("main/about.html")


@main_blueprint.route("/profile/<username>", methods=['POST', 'GET'])
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    if current_user.is_anonymous:
        return render_template('main/profile.html', user=user)
    if current_user.username == user.username:
        old_username = user.username
        form = EditProfileForm()
        if form.validate_on_submit():
            if old_username != form.username.data:
                user.username = form.username.data
            user.name = form.name.data
            user.location = form.location.data
            user.about_me = form.about_me.data
            db.session.add(user)
            db.session.commit()
            flash('Account updated!', 'success')
            return redirect(url_for('main.profile', username=user.username))
        form.username.data = user.username
        form.name.data = user.name
        form.location.data = user.location
        form.about_me.data = user.about_me
        return render_template('main/profile.html', user=user, form=form)
    elif current_user.username != user.username:
        return render_template("main/profile.html", user=user)


@main_blueprint.route("/race/<int:time>")
def race(time):
    if current_user.is_anonymous:
        user = None
    else:
        user = current_user
    if user:
        user.set_league()
    return render_template("main/race.html", user=user, time=time)

@main_blueprint.route("/post-race", methods=['POST'])
def post_race():
    if request.method == 'POST':
        points = request.values.get('points')
        username = request.values.get('username')
        if username:
            user = User.query.filter_by(username=username).first()
            if user:
                user.points += int(points)
                db.session.add(user)
                db.session.commit()
                user.set_league()
    return '', 200

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
