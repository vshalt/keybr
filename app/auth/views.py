from app.auth import auth_blueprint
from flask import render_template

@auth_blueprint.route('/register')
def register():
    return render_template('auth/register.html')

@auth_blueprint.route('/login')
def login():
    return render_template('auth/login.html')

@auth_blueprint.route('/logout')
def logout():
    return render_template('auth/logout.html')

@auth_blueprint.route('/confirm')
def confirm():
    return render_template('auth/confirm.html')
