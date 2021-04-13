from app.main import main_blueprint
from flask import render_template

@main_blueprint.app_errorhandler(404)
def error_404(e):
    return render_template('errors/404.html'), 404

@main_blueprint.app_errorhandler(403)
def error_403(e):
    return render_template('errors/403.html'), 403

@main_blueprint.app_errorhandler(500)
def error_500(e):
    return render_template('errors/500.html'), 500
