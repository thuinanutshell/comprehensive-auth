import os
from app import create_app
from flask.cli import with_appcontext
import click

app = create_app()


@app.cli.command()
@with_appcontext
def init_db():
    from flask_migrate import upgrade

    upgrade()
    click.echo("Database initialized")


@app.cli.command()
@with_appcontext
def create_tables():
    from app.database import db

    db.create_all()
    click.echo("Tables created")


if __name__ == "__main__":
    env = os.getenv("FLASK_ENV", "development")

    if env in ["development"]:
        app.run(debug=True, host="0.0.0.0", port=5000)
    elif env in ["testing"]:
        app.run(debug=False, host="127.0.0.1", port=5001)
    else:
        app.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
