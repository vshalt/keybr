from app.main import main_blueprint


@main_blueprint.route("/")
def home():
    return "<h1>Hello</h1>"
