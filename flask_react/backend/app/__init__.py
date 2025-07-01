from flask import Flask
from flask_migrate import Migrate
from models.session_model import db
from api.session_api import login_manager, bp_session
from config import DevelopmentConfig, TestingConfig, ProductionConfig

migrate = Migrate()

def create_app(config):
    app = Flask(__name__)
    app.config.update(config) # specify the config that we run the app
    
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    app.register_blueprint(bp_session)
    
    return app
    
    
    