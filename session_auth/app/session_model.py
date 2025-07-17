from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
import uuid
import re

db = SQLAlchemy()


def generate_uuid():
    """Generate a new UUID for each record"""
    return str(uuid.uuid4())


def is_valid_email(email):
    """Validate email format"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


class SessionUser(UserMixin, db.Model):
    """Table to store user's personal information

    Args:
        UserMixin (class): provides default implementations for the methods that Flask-Login expects user objects to have
        db (object): an instance of SQLAlchemy

    Attributes:
        id (str): a 32-character string converted from UUID
        first_name (str): user's first name
        last_name (str): user's last name
        username (str): username that must be unique
        email (str): valid email address
        password_hash (str): user's password that has been hashed for security
    """

    __tablename__ = "session_users"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    @staticmethod
    def set_password(password):
        """Hash password and return hash"""
        return generate_password_hash(password)

    @staticmethod
    def check_password(password_hash, password):
        """Check if password matches hash"""
        return check_password_hash(password_hash, password)

    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r"\d", password):
            return False, "Password must contain at least one number"
        return True, "Valid password"

    def __repr__(self):
        return f"User {self.first_name} {self.last_name}: \n ID: {self.id} \n username: {self.username} \n email: {self.email}"
