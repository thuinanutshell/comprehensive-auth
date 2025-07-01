import pytest
import tempfile
import os
from app import create_app
from app.model import db


@pytest.fixture(scope="session")
def app():
    """Create test application"""
    # Create temporary database
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(config="testing")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Test client"""
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_db(app):
    """Clean database before each test"""
    with app.app_context():
        db.session.query(db.Model.metadata.tables["jwt_users"]).delete()
        db.session.commit()
