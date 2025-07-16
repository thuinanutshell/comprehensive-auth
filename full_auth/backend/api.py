from flask import Flask, Blueprint, jsonify, request, url_for, session, redirect
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    get_jwt_identity,
    create_access_token,
)
from werkzeug.security import generate_password_hash, check_password_hash
from app.model import db, User
from utils import validate_required_fields
import google_auth_oauthlib.flow
import os
import json
import requests
from datetime import timedelta
import redis

jwt = JWTManager()

oauth_config = json.loads(os.environ["GOOGLE_OAUTH_SECRETS"])

oauth_flow = google_auth_oauthlib.flow.Flow.from_client_config(
    oauth_config,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
    ],
)

ACCESS_EXPIRES = timedelta(hours=24)

jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


bp_auth = Blueprint(__name__, "auth")


# Traditional Registration
@bp_auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    required_fields = ["first_name", "last_name", "username", "email", "password"]
    
    error_response = validate_required_fields(data, required_fields)
    if error_response:
        return error_response
    
    email_error = validate_email(data.get("email"))
    
    if not validate_password_strength(data.get("password")):
        return jsonify({"message": "Password must be at least 8 characters with uppercase, lowercase, and digit"}), 400

    if User.query.filter_by(username=data.get("username")).first():
        return jsonify({"message": "Username already exists"}), 400

    if User.query.filter_by(email=data.get("email")).first():
        return jsonify({"message": "Email already exists"}), 400

    new_user = User(
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        username=data.get("username"),
        email=data.get("email"),
        password_hash=generate_password_hash(data.get("password")),
        is_verified=False,
        is_active=True,
        is_oauth=False,
    )

    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id)
    
    send_verify_email(new_user.email, generate_verification_link(new_user.id))

    return (
        jsonify(
            {"message": "User registered successfully", "access_token": access_token}
        ),
        201,
    )


# Traditional Login
@bp_auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    required_fields = ["login", "password"]
    error_response = validate_required_fields(data, required_fields)
    if error_response:
        return error_response

    login_identifier = data.get("login")
    password = data.get("password")

    # Find user by username or email
    user = User.query.filter(
        (User.username == login_identifier) | (User.email == login_identifier)
    ).first()

    if not user:
        return jsonify({"message": "Invalid credentials"}), 400

    if not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid credentials"}), 400

    if not user.is_active:
        return jsonify({"message": "Account is deactivated"}), 400

    access_token = create_access_token(identity=user.id)
    return jsonify({"message": "Login successful", "access_token": access_token}), 200

# Verify email for new user
@bp_auth.route('/verify/<token>', methods=['POST'])
def verify_email(token):
    """
    The logic here is that the user will be sent a verification link after they register
    Then, when the user clicks the link, the is_verified field will be updated to True
    """
    

# OAuth
@bp_auth.route("/login/oauth")
def login_oauth():
    oauth_flow.redirect_uri = url_for("auth.oauth2callback", _external=True)
    authorization_url, state = oauth_flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@bp_auth.route("/oauth2callback")
def oauth2callback():
    if "state" not in session or session["state"] != request.args.get("state"):
        return jsonify({"error": "Invalid state parameter"}), 400

    try:
        oauth_flow.fetch_token(authorization_response=request.url)
        credentials = oauth_flow.credentials
        user_info_response = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {credentials.token}"},
        )
        user_info = user_info_response.json()

        existing_user = User.query.filter_by(email=user_info["email"]).first()
        if existing_user:
            if not existing_user.is_oauth:
                return (
                    jsonify({"error": "Account exists with different login method"}),
                    400,
                )
            user = existing_user
        else:
            user = User(
                first_name=user_info.get("given_name", ""),
                last_name=user_info.get("family_name", ""),
                username=user_info["email"],
                email=user_info["email"],
                password_hash="",
                is_verified=True,
                is_active=True,
                is_oauth=True,
            )
            db.session.add(user)
            db.session.commit()
        access_token = create_access_token(identity=user.id)
        return (
            jsonify(
                {"message": "OAuth login successful", "access_token": access_token}
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": "OAuth authentication failed"}), 400


@bp_auth.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


# Logout user
@bp_auth.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify(msg="Access token revoked")


# Update user's information
@bp_auth.route("/profile", methods=["POST"])
@jwt_required()
def update_account():
    current_user_id = get_jwt_identity()
    if not current_user:
        return jsonify({"error": "User is not authenticated"}), 404

    data = request.get_json()
    fields = ["first_name", "last_name", "username", "email", "password"]

    user = User.query.filter_by(id=current_user_id).first()
    if not user:
        jsonify({"error": "User not found"}), 404

    for field in fields:
        if data.get(field):
            if field == "password":
                setattr(user, "password_hash", generate_password_hash(data.get(field)))
            else:
                setattr(user, field, data.get(field))

    db.session.commit()
    return jsonify({"message": "User information updated successfully"}), 200


# Delete account
@bp_auth.route("/profile", methods=["DELETE"])
@jwt_required()
def delete_account():
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({"error": "User is not authenticated"}), 404

    user = User.query.filter_by(id=current_user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Add token to blocklist before deleting account
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)

    # Delete the user
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Account deleted successfully"}), 200