import os
    
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = ":memory:"
    SECRET_KEY = "test123"

class ProductionConfig: