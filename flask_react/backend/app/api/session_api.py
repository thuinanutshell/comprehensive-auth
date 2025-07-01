from flask import Flask, Blueprint, jsonify, request
from flask_login import (
    LoginManager,
    login_required,
    current_user,
    login_user,
    logout_user,
)
from app.models.session_model import db, SessionUser
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_

bp_session = Blueprint("session_auth", __name__)
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    # Retrieve the id of a user (id must be a string)
    return SessionUser.query.get(user_id)


@bp_session.route("/register", methods=["POST"])
def register():
    # Get data from the user's request
    user_data = request.get_json()
    required_fields = ["first_name", "last_name", "username", "email", "password"]
    user_info = {field: None for field in required_fields}

    for field in required_fields:
        user_info[field] = user_data.get(f"{field}")

    # Validate required fields
    for field, data in user_info.items():
        if not data or data.strip() == "":
            return jsonify({"error": f"{field} is required"}), 400

    # Check duplicate fields (username or email)
    if SessionUser.query.filter_by(username=user_info["username"]).first():
        return jsonify({"error": "Username already exists"}), 409
    if SessionUser.query.filter_by(email=user_info["email"]).first():
        return jsonify({"error": "Email already exists"}), 409

    password_hash = generate_password_hash(user_info["password"])
    new_user = SessionUser(
        first_name=user_info["first_name"],
        last_name=user_info["last_name"],
        username=user_info["username"],
        email=user_info["email"],
        password_hash=password_hash,
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "New user created successfully"}), 201


@bp_session.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    remember = data.get("remember")
    required_fields = [
        "identifier",
        "password",
    ]  # identifier can be either email or username
    login_info = {field: data.get(field) for field in required_fields}

    existing_user = SessionUser.query.filter(
        or_(
            SessionUser.username == login_info["identifier"],
            SessionUser.email == login_info["identifier"],
        )
    ).first()
    if existing_user is None:
        return jsonify({"error": "Invalid username or email"}), 401
    else:
        if check_password_hash(existing_user.password_hash, login_info["password"]):
            login_user(existing_user, remember=remember)
            return (
                jsonify(
                    {
                        "message": f"User {login_info['identifier']} logged in successfully"
                    }
                ),
                200,
            )
        else:
            return jsonify({"error": "Invalid credentials"}), 401


@bp_session.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out user successfully"}), 200


@bp_session.route("/profile/<string:user_id>", methods=["GET"])
@login_required
def get_profile(user_id):
    authenticated_user = SessionUser.query.filter_by(id=user_id).first()
    user_profile = {
        "First Name": authenticated_user.first_name,
        "Last Name": authenticated_user.last_name,
        "Username": authenticated_user.username,
        "Email": authenticated_user.email,
    }
    return (
        jsonify(
            {
                "message": f"{user_profile['Username']}'s profile retrieved successfully",
                "data": user_profile,
            }
        ),
        200,
    )
