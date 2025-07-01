from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.database import db
from app.api.session_api import login_manager, bp_session
from app.api.jwt_api import jwt_manager, bp_jwt
from config import DevelopmentConfig, TestingConfig, ProductionConfig
import os

migrate = Migrate()


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)

    if config is None:
        config = os.getenv("FLASK_ENV", "development")

    config_map = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }

    config_class = config_map.get(config.lower(), DevelopmentConfig)
    app.config.from_object(config_class)

    if config.lower() in ["production"]:
        config_class.validate()

    # Initialize extensions
    login_manager.init_app(app)
    jwt_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(bp_jwt, url_prefix="/api/jwt")

    @app.route("/")
    def check():
        return "API is running!"

    return app
