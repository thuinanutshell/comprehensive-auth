import os
import click
from flask.cli import with_appcontext
from flask_migrate import init, migrate, upgrade, downgrade
from app import create_app
from app.session_model import db

# Create app instance
app = create_app()


# Database management CLI commands
@click.command()
@with_appcontext
def init_db():
    """Initialize the migration repository."""
    try:
        init()
        click.echo("✅ Migration repository initialized.")
    except Exception as e:
        click.echo(f"❌ Error initializing migrations: {e}")


@click.command()
@click.option("--message", "-m", default="Auto migration", help="Migration message")
@with_appcontext
def migrate_db(message):
    """Generate a new migration file."""
    try:
        migrate(message=message)
        click.echo(f"✅ Migration created: {message}")
    except Exception as e:
        click.echo(f"❌ Error creating migration: {e}")


@click.command()
@with_appcontext
def upgrade_db():
    """Apply migrations to the database."""
    try:
        upgrade()
        click.echo("✅ Database upgraded successfully.")
    except Exception as e:
        click.echo(f"❌ Error upgrading database: {e}")


@click.command()
@with_appcontext
def downgrade_db():
    """Rollback the last migration."""
    try:
        downgrade()
        click.echo("✅ Database downgraded successfully.")
    except Exception as e:
        click.echo(f"❌ Error downgrading database: {e}")


@click.command()
@with_appcontext
def reset_db():
    """Reset the database (DANGER: Deletes all data!)."""
    if click.confirm("⚠️  This will delete ALL data. Are you sure?"):
        try:
            db.drop_all()
            db.create_all()
            click.echo("✅ Database reset successfully.")
        except Exception as e:
            click.echo(f"❌ Error resetting database: {e}")
    else:
        click.echo("❌ Database reset cancelled.")


@click.command()
@with_appcontext
def show_db_info():
    """Show current database information."""
    from flask import current_app

    click.echo(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    click.echo(f"Database URI: {current_app.config['SQLALCHEMY_DATABASE_URI']}")
    click.echo(f"Testing mode: {current_app.config.get('TESTING', False)}")

    # Test database connection
    try:
        from sqlalchemy import text

        result = db.session.execute(text("SELECT 1")).scalar()
        click.echo("✅ Database connection: OK")

        # Show tables
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        click.echo(f"Tables: {tables if tables else 'None'}")

    except Exception as e:
        click.echo(f"❌ Database connection failed: {e}")


# Register CLI commands
app.cli.add_command(init_db)
app.cli.add_command(migrate_db)
app.cli.add_command(upgrade_db)
app.cli.add_command(downgrade_db)
app.cli.add_command(reset_db)
app.cli.add_command(show_db_info)


if __name__ == "__main__":
    env = os.getenv("FLASK_ENV", "development")

    click.echo(f"🚀 Starting Flask app in {env} mode...")

    if env == "development":
        app.run(debug=True, host="0.0.0.0", port=5000)
    elif env == "testing":
        app.run(debug=False, host="127.0.0.1", port=5001)
    else:  # production
        app.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
