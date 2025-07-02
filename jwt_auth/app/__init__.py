from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.jwt_api import jwt_manager, bp_jwt
from app.jwt_model import db
from config import DevelopmentConfig, TestingConfig, ProductionConfig
import os

# Set up database migration when the schema changes
migrate = Migrate()


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)

    config_map = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }

    # Handle None config safely
    config_name = config or os.getenv("FLASK_ENV", "development")
    config_class = config_map.get(config_name.lower(), DevelopmentConfig)
    app.config.from_object(config_class)

    # Initialize extensions
    jwt_manager.init_app(app)
    db.init_app(app)

    if not app.config.get("TESTING"):
        migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(bp_jwt, url_prefix="/api/jwt")

    @app.route("/")
    def check():
        return f"API is running in {config} mode!"

    @app.route("/health")
    def health_check():
        try:
            from sqlalchemy import text

            db.session.execute(text("SELECT 1"))
            return {"status": "healthy", "database": "connected"}, 200
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}, 500

    with app.app_context():
        if app.config.get("TESTING"):
            db.create_all()

    with app.app_context():
        if app.config.get("TESTING"):
            db.create_all()

    return app
