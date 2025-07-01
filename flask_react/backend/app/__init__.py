from flask import Flask
from flask_migrate import Migrate
from app.models.session_model import db
from app.api.session_api import login_manager, bp_session
from config import DevelopmentConfig, TestingConfig, ProductionConfig
import os

migrate = Migrate()


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)

    if config is None:
        config = os.getenv("FLASK_ENV", "development")

    config_map = {
        "development": DevelopmentConfig,
        "dev": DevelopmentConfig,
        "testing": TestingConfig,
        "test": TestingConfig,
        "production": ProductionConfig,
        "prod": ProductionConfig,
    }

    config_class = config_map.get(config.lower(), DevelopmentConfig)
    app.config.from_object(config_class)

    if config.lower() in ["production", "prod"]:
        config_class.validate()

    # Initialize extensions
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(bp_session)
    
    @app.route('/')
    def check():
        return "API is running!"

    return app
