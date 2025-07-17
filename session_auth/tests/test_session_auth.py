import pytest
import json


@pytest.fixture
def user_data():
    """Sample user data"""
    return {
        "first_name": "Test",
        "last_name": "User",
        "username": "testuser",
        "email": "test@example.com",
        "password": "StrongPass123!",
    }


class TestRegistration:
    """Test user registration"""

    def test_register_success(self, client, user_data):
        """Test successful registration"""
        response = client.post("/api/session/register", json=user_data)

        assert response.status_code == 201
        assert "New user created successfully" in response.get_json()["message"]

    def test_register_missing_field(self, client):
        """Test registration with missing field"""
        incomplete_data = {
            "first_name": "Test",
            "email": "test@example.com",
            # Missing other required fields
        }

        response = client.post("/api/session/register", json=incomplete_data)
        assert response.status_code == 400
        assert "is required" in response.get_json()["error"]

    def test_register_invalid_email(self, client, user_data):
        """Test registration with invalid email format"""
        user_data["email"] = "invalid-email"
        response = client.post("/api/session/register", json=user_data)
        assert response.status_code == 400
        assert "Invalid email format" in response.get_json()["error"]

    def test_register_duplicate_username(self, client, user_data):
        """Test duplicate username registration"""
        # Register first user
        client.post("/api/session/register", json=user_data)

        # Try to register with same username but different email
        duplicate_data = user_data.copy()
        duplicate_data["email"] = "different@example.com"
        response = client.post("/api/session/register", json=duplicate_data)
        assert response.status_code == 409
        assert "Username already exists" in response.get_json()["error"]

    def test_register_duplicate_email(self, client, user_data):
        """Test duplicate email registration"""
        # Register first user
        client.post("/api/session/register", json=user_data)

        # Try to register with same email but different username
        duplicate_data = user_data.copy()
        duplicate_data["username"] = "differentuser"
        response = client.post("/api/session/register", json=duplicate_data)
        assert response.status_code == 409
        assert "Email already exists" in response.get_json()["error"]

    def test_register_no_json_body(self, client):
        """Test registration without JSON body"""
        response = client.post("/api/session/register")
        assert response.status_code == 400
        assert "Request must be JSON" in response.get_json()["error"]


class TestLogin:
    """Test user login"""

    def test_login_success_with_email(self, client, user_data):
        """Test successful login with email"""
        # First register user
        client.post("/api/session/register", json=user_data)

        # Then login with email
        login_data = {
            "identifier": user_data["email"],
            "password": user_data["password"],
        }
        response = client.post("/api/session/login", json=login_data)

        assert response.status_code == 200
        response_data = response.get_json()
        assert user_data["email"] in response_data["message"]

    def test_login_success_with_username(self, client, user_data):
        """Test successful login with username"""
        # First register user
        client.post("/api/session/register", json=user_data)

        # Then login with username
        login_data = {
            "identifier": user_data["username"],
            "password": user_data["password"],
        }
        response = client.post("/api/session/login", json=login_data)

        assert response.status_code == 200
        response_data = response.get_json()
        assert user_data["username"] in response_data["message"]

    def test_login_wrong_password(self, client, user_data):
        """Test login with wrong password"""
        # Register user
        client.post("/api/session/register", json=user_data)

        # Login with wrong password
        login_data = {"identifier": user_data["email"], "password": "wrongpassword"}
        response = client.post("/api/session/login", json=login_data)

        assert response.status_code == 401
        assert "Invalid credentials" in response.get_json()["error"]

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        login_data = {"identifier": "fake@example.com", "password": "StrongPass123!"}
        response = client.post("/api/session/login", json=login_data)

        assert response.status_code == 401
        assert "Invalid username or email" in response.get_json()["error"]

    def test_login_missing_fields(self, client):
        """Test login with missing required fields"""
        login_data = {"identifier": "test@example.com"}  # Missing password
        response = client.post("/api/session/login", json=login_data)

        assert response.status_code == 400
        assert "identifier and password are required" in response.get_json()["error"]

    def test_login_no_json_body(self, client):
        """Test login without JSON body"""
        response = client.post("/api/session/login")
        assert response.status_code == 400
        assert "Request must be JSON" in response.get_json()["error"]


class TestProfile:
    """Test profile access"""

    def test_get_profile_success(self, client, user_data):
        """Test successful profile access"""
        # Register and login user
        client.post("/api/session/register", json=user_data)
        login_data = {
            "identifier": user_data["email"],
            "password": user_data["password"],
        }
        client.post("/api/session/login", json=login_data)

        # Get profile
        response = client.get("/api/session/profile")

        assert response.status_code == 200
        response_data = response.get_json()
        assert "data" in response_data

        profile = response_data["data"]
        assert profile["email"] == user_data["email"]
        assert profile["username"] == user_data["username"]
        assert profile["first_name"] == user_data["first_name"]
        assert profile["last_name"] == user_data["last_name"]


class TestLogout:
    """Test logout functionality"""

    def get_auth_token(self, client, user_data):
        """Helper to get auth token"""
        client.post("/api/session/register", json=user_data)
        login_data = {
            "identifier": user_data["email"],
            "password": user_data["password"],
        }
        response = client.post("/api/session/login", json=login_data)

    def test_logout_success(self, client, user_data):
        """Test successful logout"""
        self.get_auth_token(client, user_data)
        response = client.post("/api/session/logout")
        assert response.status_code == 200


class TestWorkflow:
    """Test complete user workflow"""

    def test_complete_flow(self, client, user_data):
        """Test register -> login -> profile -> logout -> blocked access"""
        # 1. Register
        register_response = client.post("/api/session/register", json=user_data)
        assert register_response.status_code == 201

        # 2. Login
        login_data = {
            "identifier": user_data["email"],
            "password": user_data["password"],
        }
        login_response = client.post("/api/session/login", json=login_data)
        assert login_response.status_code == 200

        # 3. Get profile
        profile_response = client.get("/api/session/profile")
        assert profile_response.status_code == 200

        # Verify profile data
        profile_data = profile_response.get_json()["data"]
        assert profile_data["email"] == user_data["email"]

        # 4. Logout
        logout_response = client.post("/api/session/logout")
        assert logout_response.status_code == 200

        # 5. Verify token is blocked
        final_response = client.get("/api/session/profile")
        assert final_response.status_code in [401, 302]

    def test_multiple_login_logout_cycles(self, client, user_data):
        """Test multiple login/logout cycles work correctly"""
        # Register user once
        client.post("/api/session/register", json=user_data)

        login_data = {
            "identifier": user_data["email"],
            "password": user_data["password"],
        }

        # Test 3 cycles
        for i in range(3):
            # Login
            login_response = client.post("/api/session/login", json=login_data)
            assert login_response.status_code == 200

            profile_response = client.get("/api/session/profile")
            assert profile_response.status_code == 200

            # Logout
            logout_response = client.post("/api/session/logout")
            assert logout_response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
