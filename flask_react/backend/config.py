import os


class BaseConfig:
    """Base configuration with common settings"""

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_ALGORITHM = "HS256"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URI", "sqlite:///development.db")
    SECRET_KEY = os.getenv("DEV_SECRET_KEY", "dev-secret-key-change-in-production")


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SECRET_KEY = "test-secret-key"


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")
