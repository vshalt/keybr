from app.main import main_blueprint
from flask import render_template

@main_blueprint.app_errorhandler(400)
def error_404(e):
    return render_template('errors/404.html'), e

@main_blueprint.app_errorhandler(403)
def error_403(e):
    return render_template('errors/403.html'), e

@main_blueprint.app_errorhandler(500)
def error_500(e):
    return render_template('errors/500.html'), e
