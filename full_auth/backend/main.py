from flask import Flask
from flask_cors import CORS
from model import db
from api import bp_auth, jwt
import os
from datetime import timedelta
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "your-secret-key-here")

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///app.db"  # Default to SQLite for development
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # JWT configuration
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", app.config["SECRET_KEY"])
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

    # SendGrid configuration
    app.config["SENDGRID_API_KEY"] = os.getenv("SENDGRID_API_KEY")
    app.config["SENDGRID_FROM_EMAIL"] = os.getenv("SENDGRID_FROM_EMAIL")

    # Session configuration for OAuth
    app.config["SESSION_COOKIE_SECURE"] = (
        os.getenv("SESSION_COOKIE_SECURE", "False").lower() == "true"
    )
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Enable CORS for frontend integration
    CORS(app, origins=os.getenv("FRONTEND_URL", "http://localhost:3000"))

    # Register blueprints
    app.register_blueprint(bp_auth, url_prefix="/api/auth")

    # Create tables
    with app.app_context():
        db.create_all()

    # Health check endpoint
    @app.route("/health")
    def health_check():
        return {"status": "healthy", "message": "API is running"}, 200

    # Root endpoint
    @app.route("/")
    def index():
        return {"message": "Welcome to the Authentication API"}, 200

    return app


if __name__ == "__main__":
    app = create_app()

    # Development server settings
    debug_mode = os.getenv("DEBUG", "True").lower() == "true"
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))

    app.run(debug=debug_mode, host=host, port=port)
