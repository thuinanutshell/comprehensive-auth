import os
import re
from typing import List, Optional, Tuple
from flask import jsonify
from email_validator import validate_email, EmailNotValidError
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import secrets
from datetime import datetime, timedelta

mail = Mail()


def validate_required_fields(data: dict, required_fields: List[str]) -> Optional[Tuple]:
    for field in required_fields:
        if not data.get(f"{field}"):
            return jsonify({"message": f"{field} is required"}), 400
    return None


def validate_email(email: str):
    try:
        emailinfo = validate_email(email, check_deliverability=False)
        return None
    except EmailNotValidError as e:
        return str(e)


def validate_password_strength(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    return True


def generate_verification_link(user_id):
    serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
    token = serializer.dumps(user_id, salt="email-verification-salt")
    return f"{os.getenv('FRONTEND_URL')}/verify/{token}"


def generate_reset_password_link(user_id):
    """Generate a secure token for password reset."""
    serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
    token = serializer.dumps(user_id, salt="reset-password-salt")
    return f"{os.getenv('FRONTEND_URL')}/reset-password/{token}"


def send_verify_email(receiver: str, link):
    msg = Message(
        subject="Verification Email",
        sender=os.getenv("SENDER_EMAIL"),
        recipients=[receiver],
    )
    msg.body = f"Please click this {link} to verify your email"
    mail.send(msg)
    return "Sent"


def send_reset_password_email():
    msg = Message(
        subject="Reset Password Email",
        sender=os.getenv("SENDER_EMAIL"),
        recipients=[receiver],
    )
    reset_link = f"{os.getenv('FRONTEND_URL')}/reset-password/{token}"
    msg.body = f"Please click this link to reset your password: {reset_link}"
    mail.send(msg)
    return "Sent"


def verify_token(token: str, salt: str, max_age: int = 3600):
    """Verify and decode a token with given salt and max age."""
    try:
        serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
        user_id = serializer.loads(token, salt=salt, max_age=max_age)
        return user_id, None
    except Exception as e:
        return None, str(e)
