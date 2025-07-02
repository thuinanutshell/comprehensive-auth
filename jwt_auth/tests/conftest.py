import pytest
import sys
import os

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.jwt_model import db, JWTUser


@pytest.fixture
def app():
    """Create test application with in-memory database"""
    app = create_app(config="testing")

    with app.app_context():
        # Tables are already created by create_app for testing
        yield app
        # Clean up after test
        db.session.remove()


@pytest.fixture
def client(app):
    """Test client"""
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_db(app):
    """Clean database before each test"""
    with app.app_context():
        # Clear all users before each test
        db.session.query(JWTUser).delete()
        db.session.commit()
