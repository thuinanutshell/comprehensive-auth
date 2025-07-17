import os
from datetime import timedelta


class BaseConfig:
    """Base configuration with common settings"""

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True


class DevelopmentConfig(BaseConfig):
    """Development configuration"""

    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URI", "sqlite:///development.db")
    SECRET_KEY = os.getenv("DEV_SECRET_KEY", "dev-secret-change-in-production")


class ProductionConfig(BaseConfig):
    """Production configuration"""

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URI", "sqlite:///production.db")
    SECRET_KEY = os.getenv("PROD_SECRET_KEY")

    # Validation for production
    def __init__(self):
        if not os.getenv("PROD_SECRET_KEY"):
            raise ValueError("PROD_SECRET_KEY must be set in production")


class TestingConfig(BaseConfig):
    """Testing configuration"""

    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SECRET_KEY = "test-jwt-secret-key-123"
    WTF_CSRF_ENABLED = False
