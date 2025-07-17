import os
import re
from typing import List, Optional, Tuple
from flask import jsonify
from email_validator import validate_email, EmailNotValidError
from itsdangerous import URLSafeTimedSerializer
import secrets
from datetime import datetime, timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

# Initialize SendGrid client
sg = SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))


def validate_required_fields(data: dict, required_fields: List[str]) -> Optional[Tuple]:
    for field in required_fields:
        if not data.get(f"{field}"):
            return jsonify({"message": f"{field} is required"}), 400
    return None


def validate_email_field(email: str):
    try:
        emailinfo = validate_email(email)
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


def send_email_with_sendgrid(
    to_email: str, subject: str, html_content: str, plain_content: str = None
):
    """
    Send email using SendGrid API
    """
    try:
        from_email = Email(os.getenv("SENDGRID_FROM_EMAIL"))
        to_email = To(to_email)

        # Use HTML content primarily, fallback to plain text
        content = Content("text/html", html_content)

        mail = Mail(from_email, to_email, subject, content)

        # Add plain text version if provided
        if plain_content:
            mail.add_content(Content("text/plain", plain_content))

        response = sg.send(mail)

        if response.status_code == 202:
            return True, "Email sent successfully"
        else:
            return False, f"Failed to send email: {response.status_code}"

    except Exception as e:
        return False, f"Error sending email: {str(e)}"


def send_verify_email(receiver: str, link: str):
    """Send verification email using SendGrid"""
    subject = "Verify Your Email Address"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Email Verification</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; background-color: #f9f9f9; }}
            .button {{ 
                display: inline-block; 
                padding: 12px 24px; 
                background-color: #4CAF50; 
                color: white; 
                text-decoration: none; 
                border-radius: 4px; 
                margin: 20px 0;
            }}
            .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Email Verification</h1>
            </div>
            <div class="content">
                <p>Hello!</p>
                <p>Thank you for registering with us. To complete your registration, please verify your email address by clicking the button below:</p>
                <p style="text-align: center;">
                    <a href="{link}" class="button">Verify Email Address</a>
                </p>
                <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #666;">{link}</p>
                <p>This verification link will expire in 1 hour for security reasons.</p>
                <p>If you didn't create an account with us, please ignore this email.</p>
            </div>
            <div class="footer">
                <p>This is an automated message, please do not reply to this email.</p>
            </div>
        </div>
    </body>
    </html>
    """

    plain_content = f"""
    Email Verification
    
    Hello!
    
    Thank you for registering with us. To complete your registration, please verify your email address by clicking the link below:
    
    {link}
    
    This verification link will expire in 1 hour for security reasons.
    
    If you didn't create an account with us, please ignore this email.
    
    This is an automated message, please do not reply to this email.
    """

    success, message = send_email_with_sendgrid(
        receiver, subject, html_content, plain_content
    )

    if not success:
        print(f"Failed to send verification email: {message}")

    return success, message


def send_reset_password_email(receiver: str, token: str):
    """Send password reset email using SendGrid"""
    subject = "Reset Your Password"
    reset_link = f"{os.getenv('FRONTEND_URL')}/reset-password/{token}"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Password Reset</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #f44336; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; background-color: #f9f9f9; }}
            .button {{ 
                display: inline-block; 
                padding: 12px 24px; 
                background-color: #f44336; 
                color: white; 
                text-decoration: none; 
                border-radius: 4px; 
                margin: 20px 0;
            }}
            .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Password Reset</h1>
            </div>
            <div class="content">
                <p>Hello!</p>
                <p>We received a request to reset your password. If you made this request, please click the button below to reset your password:</p>
                <p style="text-align: center;">
                    <a href="{reset_link}" class="button">Reset Password</a>
                </p>
                <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #666;">{reset_link}</p>
                <p>This reset link will expire in 1 hour for security reasons.</p>
                <p>If you didn't request a password reset, please ignore this email. Your password will remain unchanged.</p>
            </div>
            <div class="footer">
                <p>This is an automated message, please do not reply to this email.</p>
            </div>
        </div>
    </body>
    </html>
    """

    plain_content = f"""
    Password Reset
    
    Hello!
    
    We received a request to reset your password. If you made this request, please click the link below to reset your password:
    
    {reset_link}
    
    This reset link will expire in 1 hour for security reasons.
    
    If you didn't request a password reset, please ignore this email. Your password will remain unchanged.
    
    This is an automated message, please do not reply to this email.
    """

    success, message = send_email_with_sendgrid(
        receiver, subject, html_content, plain_content
    )

    if not success:
        print(f"Failed to send password reset email: {message}")

    return success, message


def verify_token(token: str, salt: str, max_age: int = 3600):
    """Verify and decode a token with given salt and max age."""
    try:
        serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
        user_id = serializer.loads(token, salt=salt, max_age=max_age)
        return user_id, None
    except Exception as e:
        return None, str(e)
