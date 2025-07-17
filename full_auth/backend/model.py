from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean, Index
from sqlalchemy.orm import relationship, mapped_column, Mapped
import uuid

db = SQLAlchemy()


def generate_uuid():
    return str(uuid.uuid4())  # Convert to string for consistency


class User(db.Model):
    __tablename__ = "user"

    # Add indexes for performance
    __table_args__ = (
        Index("idx_user_email", "email"),
        Index("idx_user_username", "username"),
    )

    # User's basic information
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=True)

    # Boolean field to check if the user email is verified and if the user is active
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_oauth: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    def get_user_id(self):
        return self.id
