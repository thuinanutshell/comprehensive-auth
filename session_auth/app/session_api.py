from flask import Flask, Blueprint, jsonify, request
from flask_login import (
    LoginManager,
    login_required,
    current_user,
    login_user,
    logout_user,
)
from app.session_model import db, SessionUser, is_valid_email
from sqlalchemy import or_

bp_session = Blueprint("session_auth", __name__)
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return SessionUser.query.get(user_id)


@bp_session.route("/register", methods=["POST"])
def register():
    # Validate JSON request
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    user_data = request.get_json()
    if not user_data:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ["first_name", "last_name", "username", "email", "password"]
    user_info = {}

    # Validate required fields
    for field in required_fields:
        value = user_data.get(field)
        if not value or not str(value).strip():
            return jsonify({"error": f"{field} is required"}), 400
        user_info[field] = str(value).strip()

    # Validate email format
    if not is_valid_email(user_info["email"]):
        return jsonify({"error": "Invalid email format"}), 400

    # Validate password strength
    is_valid, message = SessionUser.validate_password(user_info["password"])
    if not is_valid:
        return jsonify({"error": message}), 400

    # Check for duplicates
    if SessionUser.query.filter_by(username=user_info["username"]).first():
        return jsonify({"error": "Username already exists"}), 409
    if SessionUser.query.filter_by(email=user_info["email"]).first():
        return jsonify({"error": "Email already exists"}), 409

    try:
        new_user = SessionUser(
            first_name=user_info["first_name"],
            last_name=user_info["last_name"],
            username=user_info["username"],
            email=user_info["email"],
            password_hash=SessionUser.set_password(user_info["password"]),
        )

        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "New user created successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Registration failed"}), 500


@bp_session.route("/login", methods=["POST"])
def login():
    # Validate JSON request
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    identifier = data.get("identifier")
    password = data.get("password")
    remember = data.get("remember", False)

    if not identifier or not password:
        return jsonify({"error": "identifier and password are required"}), 400

    existing_user = SessionUser.query.filter(
        or_(
            SessionUser.username == identifier,
            SessionUser.email == identifier,
        )
    ).first()

    if not existing_user:
        return jsonify({"error": "Invalid username or email"}), 401

    if not SessionUser.check_password(existing_user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    login_user(existing_user, remember=remember)
    return jsonify({"message": f"User {identifier} logged in successfully"}), 200


@bp_session.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out user successfully"}), 200


@bp_session.route("/profile", methods=["GET"])
@login_required
def get_profile():
    authenticated_user = current_user
    user_profile = {
        "first_name": authenticated_user.first_name,
        "last_name": authenticated_user.last_name,
        "username": authenticated_user.username,
        "email": authenticated_user.email,
    }
    return (
        jsonify(
            {
                "message": f"{user_profile['username']}'s profile retrieved successfully",
                "data": user_profile,
            }
        ),
        200,
    )
