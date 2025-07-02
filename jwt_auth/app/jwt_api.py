from flask import Flask, Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager,
    get_jwt,
)
from app.jwt_model import db, JWTUser
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
import redis
import re
from datetime import timedelta

# After 24 hours since logged in, user's token will be automatically revoked
ACCESS_EXPIRES = timedelta(hours=24)
jwt_manager = JWTManager()

bp_jwt = Blueprint("jwt_auth", __name__)


def get_redis_client():
    """Get Redis client from current app configuration"""
    from flask import current_app

    redis_url = current_app.config.get("REDIS_URL")
    return redis.from_url(redis_url, decode_responses=True)


@jwt_manager.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    """Check if a JWT token is in the blocklist"""
    jti = jwt_payload["jti"]
    redis_client = get_redis_client()
    token_in_redis = redis_client.get(jti)
    return token_in_redis is not None


@bp_jwt.route("/register", methods=["POST"])
def register():
    """Register a new user"""
    try:
        # Check if request has JSON content type first
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        # Get data from the user's request
        user_data = request.get_json()
        if user_data is None:
            return jsonify({"error": "Request body must contain valid JSON"}), 400

        required_fields = ["first_name", "last_name", "username", "email", "password"]
        user_info = {field: None for field in required_fields}

        for field in required_fields:
            user_info[field] = user_data.get(field)

        # Validate required fields
        for field, data in user_info.items():
            if not data or str(data).strip() == "":
                return jsonify({"error": f"{field} is required"}), 400

        # Validate email format
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, user_info["email"]):
            return jsonify({"error": "Invalid email format"}), 400

        # Check duplicate fields (username or email)
        if JWTUser.query.filter_by(username=user_info["username"]).first():
            return jsonify({"error": "Username already exists"}), 409
        if JWTUser.query.filter_by(email=user_info["email"]).first():
            return jsonify({"error": "Email already exists"}), 409

        # Create new user
        password_hash = generate_password_hash(user_info["password"])
        new_user = JWTUser(
            first_name=user_info["first_name"],
            last_name=user_info["last_name"],
            username=user_info["username"],
            email=user_info["email"],
            password_hash=password_hash,
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "New user created successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@bp_jwt.route("/login", methods=["POST"])
def login():
    """Login user and return access token"""
    try:
        # Check if request has JSON content type first
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        # Get data from the user's request
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Request body must contain valid JSON"}), 400

        # Get identifier (can be username or email) and password
        required_fields = ["identifier", "password"]
        login_info = {field: data.get(field) for field in required_fields}

        # Validate required fields
        for field, value in login_info.items():
            if not value:
                return jsonify({"error": f"{field} is required"}), 400

        # Check if the user exists
        existing_user = JWTUser.query.filter(
            or_(
                JWTUser.username == login_info["identifier"],
                JWTUser.email == login_info["identifier"],
            )
        ).first()

        if existing_user is None:
            return jsonify({"error": "Invalid username or email"}), 401

        # Check password
        if check_password_hash(existing_user.password_hash, login_info["password"]):
            access_token = create_access_token(identity=existing_user.id)
            return (
                jsonify(
                    {
                        "message": f"User {login_info['identifier']} logged in successfully",
                        "access_token": access_token,
                    }
                ),
                200,
            )
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@bp_jwt.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    """Logout user by adding token to blocklist"""
    try:
        jti = get_jwt()["jti"]
        redis_client = get_redis_client()
        redis_client.set(jti, "", ex=ACCESS_EXPIRES)
        return jsonify({"message": "Access token revoked"}), 200
    except Exception as e:
        return jsonify({"error": "Logout failed"}), 500


@bp_jwt.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    """Get current user's profile"""
    try:
        current_user_id = get_jwt_identity()
        current_user = db.session.get(JWTUser, current_user_id)

        if not current_user:
            return jsonify({"error": "User not found"}), 404

        user_profile = {
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "username": current_user.username,
            "email": current_user.email,
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

    except Exception as e:
        return jsonify({"error": "Failed to retrieve profile"}), 500
