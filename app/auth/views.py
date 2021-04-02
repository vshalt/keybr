from flask import render_template, abort, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user
from app import db
from app.auth import auth_blueprint
from app.mail import send_mail
from app.models import User
from app.auth.forms import (
    ChangePasswordForm,
    RegisterForm,
    ChangeUsernameForm,
    RequestForgotPasswordForm,
    ChangeEmailForm,
    NewPasswordForm
)

@auth_blueprint.route('/register')
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_mail(
            template='mail/register',
            to=user.email,
            subject='Confirm account',
            token=token, user=user
        )
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth_blueprint.route('/login')
def login():
    return render_template('auth/login.html')

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out')
    return redirect(url_for('main.home'))

@auth_blueprint.route('/confirm')
@login_required
def get_confirmation():
    if current_user.is_confirmed:
        flash('Email already confirmed')
        return redirect(url_for('main.home'))
    token = current_user.generate_confirmation_token()
    send_mail(
        template='mail/confirm_account',
        to=current_user.email,
        subject='Confirm email',
        token = token,
        user = current_user
    )
    flash('Email sent')
    return redirect(url_for('main.home'))

@auth_blueprint.route('/confirm/<token>')
@login_required
def verify_token(token):
    if current_user.is_confirmed:
        flash('Email already confirmed!')
        return redirect(url_for('main.home'))
    if current_user.confirm_token(token):
        db.session.commit()
        flash('Account confirmed!')
    else:
        flash('An error occurred, try again later!')
    return render_template('auth/confirm.html')

@auth_blueprint.route('/change-pass/<username>')
@login_required
def reset_password(username):
    if current_user.username != username:
        abort(403)
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if user.change_password(form.old_password.data, form.new_password.data):
            db.session.commit()
            flash('Password changed successfully. Login to continue')
            return redirect(url_for('main.home'))
        flash('Old password is not correct. Try again')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

@auth_blueprint.route('/change-username/<username>')
@login_required
def change_username(username):
    if current_user.username != username:
        abort(403)
    form = ChangeUsernameForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            current_user.username = form.username.data
            db.session.add(current_user)
            db.session.commit()
            flash('Username changed successfully')
            return redirect(url_for('main.home'))
        flash('Check password and try again')
    return render_template('auth/change_username.html', form=form)

@auth_blueprint.route('/forgot')
def request_forgot_password():
    form = RequestForgotPasswordForm()
    if form.validate_on_submit():
        token = current_user.generate_forgot_password_token()
        send_mail(
            template='mail/forgot_password',
            to=form.email.data,
            subject='Password reset',
            token = token
        )
        flash('Email sent')
        return redirect(url_for('main.home'))
    return render_template('auth/request_forgot_password.html')

@auth_blueprint.route('/forgot/<token>')
def forgot_password(token):
    if current_user.confirm_forgot_password_token(token):
        form = NewPasswordForm()
        if form.validate_on_submit():
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Password changed successfully. Login to continue')
            return redirect(url_for('main.home'))
    flash('An error occurred, try again')
    return redirect(url_for('main.home'))
        

@auth_blueprint.route('/change-email/<username>')
@login_required
def request_change_email(username):
    if current_user.username != username:
        abort(403)
    form = ChangeEmailForm()
    if form.validate_on_submit():
        token = current_user.generate_change_email_token(form.new_email.data)
        send_mail(
            template='mail/change_email',
            to=current_user.email,
            subject='Change email',
            token=token,
        )
        flash('Email sent')
        return redirect(url_for('main.home'))
    form.old_email.data = current_user.email
    return render_template('auth/request_change_email.html')

@auth_blueprint.route('/change-email/<username>/<token>')
@login_required
def change_email(username, token):
    if current_user.username != username:
        abort(403)
    if current_user.confirm_change_email_token(token):
        db.session.commit()
        flash('Email changed successfully')
        return redirect(url_for('main.home'))
    flash('An error occurred, try again later')
    return redirect(url_for('main.home'))
