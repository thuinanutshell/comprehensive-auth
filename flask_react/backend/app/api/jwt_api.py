from flask import Flask, Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager,
)
from app.models.session_model import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
import redis
from datetime import timedelta

ACCESS_EXPIRES = timedelta(hours=24)
bp_jwt = Blueprint("jwt_auth", __name__)
jwt = JWTManager()

jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


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
    if User.query.filter_by(username=user_info["username"]).first():
        return jsonify({"error": "Username already exists"}), 409
    if User.query.filter_by(email=user_info["email"]).first():
        return jsonify({"error": "Email already exists"}), 409

    password_hash = generate_password_hash(user_info["password"])
    new_user = User(
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

    existing_user = User.query.filter(
        or_(
            User.username == login_info["identifier"],
            User.email == login_info["identifier"],
        )
    ).first()
    if existing_user is None:
        return jsonify({"error": "Invalid username or email"}), 401
    else:
        if check_password_hash(existing_user.password_hash, login_info["password"]):
            access_token = create_access_token(identity=existing_user.id)
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


@app.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify(msg="Access token revoked")


@bp_session.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    current_user = get_jwt_identity()
    user_profile = {
        "First Name": current_user.first_name,
        "Last Name": current_user.last_name,
        "Username": current_user.username,
        "Email": current_user.email,
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
