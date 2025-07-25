from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
import uuid

db = SQLAlchemy()


def generate_uuid():
    """Generate a new UUID for each record"""
    return str(uuid.uuid4())


class JWTUser(db.Model):
    """Table to store user's personal information

    Args:
        db (object): an instance of SQLAlchemy
        id (str): a 32-character string converted from UUID (must be string to be compatible with JWT)
        first_name (str): user's first name
        last_name (str): user's last name
        username (str): username that must be unique
        email (str): valid email address
        password_hash (str): user's password that has been hashed for security
    """

    __tablename__ = "jwt_users"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    # String representation of an user object
    def __repr__(self):
        return f"User {self.first_name} {self.last_name}: \n ID: {self.id} \n username: {self.username} \n email: {self.email}"
