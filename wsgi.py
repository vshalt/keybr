from app import create_app, db
from app.models import User
from flask_migrate import upgrade

app = create_app("development")

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)

@app.cli.command()
def deploy():
    upgrade()
