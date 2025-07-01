from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
import uuid

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Table to store user's personal information

    Args:
        db (object): an instance of SQLAlchemy
        id (str): a 32-character string converted from UUID
        first_name (str): user's first name
        last_name (str): user's last name
        username (str): username that must be unique
        email (str): valid email address
        password_hash (str): user's password that has been hashed for security
    """
    id: Mapped[str] = mapped_column(String, primary_key=True, default=str(uuid.uuid4()))
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    
    # String representation of an user object
    def __repr__(self):
        return f"User {self.first_name} {self.last_name}: \n ID: {self.id} \n username: {self.username} \n email: {self.email}"
