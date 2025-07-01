import pytest
import json
from app import create_app
from app.models.jwt_model import db


@pytest.fixture
def app():
    """Create test app"""
    app = create_app(config="testing")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Test client"""
    return app.test_client()


@pytest.fixture
def user_data():
    """Sample user data"""
    return {
        "first_name": "Test",
        "last_name": "User",
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
    }


class TestRegistration:
    """Test user registration"""

    def test_register_success(self, client, user_data):
        """Test successful registration"""
        response = client.post("/api/jwt/register", json=user_data)

        assert response.status_code == 201
        assert "New user created successfully" in response.get_json()["message"]

    def test_register_missing_field(self, client):
        """Test registration with missing field"""
        incomplete_data = {
            "first_name": "Test",
            "email": "test@example.com",
            # Missing other fields
        }

        response = client.post("/api/jwt/register", json=incomplete_data)
        assert response.status_code == 400

    def test_register_duplicate_user(self, client, user_data):
        """Test duplicate user registration"""
        # Register first user
        client.post("/api/jwt/register", json=user_data)

        # Try to register same user again
        response = client.post("/api/jwt/register", json=user_data)
        assert response.status_code == 409


class TestLogin:
    """Test user login"""

    def test_login_success(self, client, user_data):
        """Test successful login"""
        # First register user
        client.post("/api/jwt/register", json=user_data)

        # Then login
        login_data = {
            "identifier": user_data["email"],
            "password": user_data["password"],
        }
        response = client.post("/api/jwt/login", json=login_data)

        assert response.status_code == 200
        assert "access_token" in response.get_json()

    def test_login_wrong_password(self, client, user_data):
        """Test login with wrong password"""
        # Register user
        client.post("/api/jwt/register", json=user_data)

        # Login with wrong password
        login_data = {"identifier": user_data["email"], "password": "wrongpassword"}
        response = client.post("/api/jwt/login", json=login_data)

        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        login_data = {"identifier": "fake@example.com", "password": "password123"}
        response = client.post("/api/jwt/login", json=login_data)

        assert response.status_code == 401


class TestProfile:
    """Test profile access"""

    def get_auth_token(self, client, user_data):
        """Helper to get auth token"""
        client.post("/api/jwt/register", json=user_data)
        login_data = {
            "identifier": user_data["email"],
            "password": user_data["password"],
        }
        response = client.post("/api/jwt/login", json=login_data)
        return response.get_json()["access_token"]

    def test_get_profile_success(self, client, user_data):
        """Test successful profile access"""
        token = self.get_auth_token(client, user_data)
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/api/jwt/profile", headers=headers)

        assert response.status_code == 200
        profile = response.get_json()["data"]
        assert profile["Email"] == user_data["email"]
        assert profile["Username"] == user_data["username"]

    def test_get_profile_no_token(self, client):
        """Test profile access without token"""
        response = client.get("/api/jwt/profile")
        assert response.status_code == 401

    def test_get_profile_invalid_token(self, client):
        """Test profile access with invalid token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/jwt/profile", headers=headers)
        assert response.status_code in [401, 422]


class TestLogout:
    """Test logout functionality"""

    def get_auth_token(self, client, user_data):
        """Helper to get auth token"""
        client.post("/api/jwt/register", json=user_data)
        login_data = {
            "identifier": user_data["email"],
            "password": user_data["password"],
        }
        response = client.post("/api/jwt/login", json=login_data)
        return response.get_json()["access_token"]

    def test_logout_success(self, client, user_data):
        """Test successful logout"""
        token = self.get_auth_token(client, user_data)
        headers = {"Authorization": f"Bearer {token}"}

        response = client.delete("/api/jwt/logout", headers=headers)
        assert response.status_code == 200

    def test_logout_blocks_token(self, client, user_data):
        """Test that logout blocks token from further use"""
        token = self.get_auth_token(client, user_data)
        headers = {"Authorization": f"Bearer {token}"}

        # Logout
        client.delete("/api/jwt/logout", headers=headers)

        # Try to use token again
        response = client.get("/api/jwt/profile", headers=headers)
        assert response.status_code == 401


class TestWorkflow:
    """Test complete user workflow"""

    def test_complete_flow(self, client, user_data):
        """Test register -> login -> profile -> logout"""
        # 1. Register
        register_response = client.post("/api/jwt/register", json=user_data)
        assert register_response.status_code == 201

        # 2. Login
        login_data = {
            "identifier": user_data["email"],
            "password": user_data["password"],
        }
        login_response = client.post("/api/jwt/login", json=login_data)
        assert login_response.status_code == 200

        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 3. Get profile
        profile_response = client.get("/api/jwt/profile", headers=headers)
        assert profile_response.status_code == 200

        # 4. Logout
        logout_response = client.delete("/api/jwt/logout", headers=headers)
        assert logout_response.status_code == 200

        # 5. Verify token is blocked
        final_response = client.get("/api/jwt/profile", headers=headers)
        assert final_response.status_code == 401


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
