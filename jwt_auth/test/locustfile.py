"""
Simple Performance Test: JWT vs Session Authentication
Save this as: tests/performance/locustfile.py

Usage:
    cd flask_react/backend
    locust -f tests/performance/locustfile.py --host=http://127.0.0.1:5001
"""

import random
import string
from locust import HttpUser, task, between


# Configuration
BASE_CONFIG = {
    "jwt_endpoints": {
        "register": "/api/jwt/register",
        "login": "/api/jwt/login",
        "profile": "/api/jwt/profile",
        "logout": "/api/jwt/logout",
    },
    "session_endpoints": {
        "register": "/api/session/register",
        "login": "/api/session/login",
        "profile": "/api/session/profile",
        "logout": "/api/session/logout",
    },
}


# Utility Functions
def generate_unique_user_data():
    """Generate unique user data for registration"""
    random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return {
        "first_name": f"test{random_suffix}",
        "last_name": f"user{random_suffix}",
        "username": f"user_{random_suffix}",
        "email": f"user_{random_suffix}@test.com",
        "password": "testpassword123!",
    }


# Base User Class
class BaseAuthUser(HttpUser):
    """Base class with common authentication testing methods"""

    abstract = True
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests

    def on_start(self):
        """Called when a user starts - registers and logs in"""
        self.user_data = generate_unique_user_data()
        self.register_user()
        self.login_user()

    def register_user(self):
        """Register a new user - implement in subclass"""
        raise NotImplementedError

    def login_user(self):
        """Login user - implement in subclass"""
        raise NotImplementedError

    def get_profile(self):
        """Get user profile - most frequent operation"""
        raise NotImplementedError

    def logout_and_login(self):
        """Occasionally logout and login again"""
        self.logout_user()
        self.login_user()

    def logout_user(self):
        """Logout user - implement in subclass"""
        raise NotImplementedError


# JWT Authentication User
class JWTAuthUser(BaseAuthUser):
    """Test JWT-based authentication performance"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.access_token = None

    def register_user(self):
        """Register user via JWT endpoint"""
        response = self.client.post(
            BASE_CONFIG["jwt_endpoints"]["register"],
            json=self.user_data,
            name="JWT Register",
        )
        if response.status_code != 201:
            print(f"JWT Registration failed: {response.status_code}")

    def login_user(self):
        """Login via JWT and store token"""
        login_data = {
            "identifier": self.user_data["email"],
            "password": self.user_data["password"],
        }

        with self.client.post(
            BASE_CONFIG["jwt_endpoints"]["login"],
            json=login_data,
            name="JWT Login",
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                self.access_token = response.json().get("access_token")
                if not self.access_token:
                    response.failure("No access token in response")
            else:
                response.failure(f"Login failed: {response.status_code}")

    @task(3)
    def get_profile(self):
        """Get profile using JWT token"""
        if not self.access_token:
            return

        headers = {"Authorization": f"Bearer {self.access_token}"}
        self.client.get(
            BASE_CONFIG["jwt_endpoints"]["profile"],
            headers=headers,
            name="JWT Get Profile",
        )

    def logout_user(self):
        """Logout and invalidate JWT token"""
        if not self.access_token:
            return

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = self.client.delete(
            BASE_CONFIG["jwt_endpoints"]["logout"], headers=headers, name="JWT Logout"
        )
        if response.status_code == 200:
            self.access_token = None


# Session Authentication User
class SessionAuthUser(BaseAuthUser):
    """Test Session-based authentication performance"""

    def register_user(self):
        """Register user via session endpoint"""
        response = self.client.post(
            BASE_CONFIG["session_endpoints"]["register"],
            json=self.user_data,
            name="Session Register",
        )
        if response.status_code != 201:
            print(f"Session Registration failed: {response.status_code}")

    def login_user(self):
        """Login via session (cookies automatically handled)"""
        login_data = {
            "identifier": self.user_data["email"],
            "password": self.user_data["password"],
        }

        self.client.post(
            BASE_CONFIG["session_endpoints"]["login"],
            json=login_data,
            name="Session Login",
        )

    @task(3)
    def get_profile(self):
        """Get profile using session cookies"""
        self.client.get(
            BASE_CONFIG["session_endpoints"]["profile"], name="Session Get Profile"
        )

    def logout_user(self):
        """Logout and clear session"""
        self.client.post(
            BASE_CONFIG["session_endpoints"]["logout"], name="Session Logout"
        )


# Test Scenarios


class JWTOnlyTest(JWTAuthUser):
    """Test only JWT authentication - uncomment to use"""

    weight = 1


# class SessionOnlyTest(SessionAuthUser):
#     """Test only Session authentication - uncomment to use"""
#     weight = 1

# class MixedAuthTest(HttpUser):
#     """Test both authentication methods simultaneously"""
#     weight = 1
#     wait_time = between(1, 3)

#     def on_start(self):
#         """Randomly assign authentication method to this user"""
#         if random.choice([True, False]):
#             self.auth_user = JWTAuthUser()
#             self.auth_type = "JWT"
#         else:
#             self.auth_user = SessionAuthUser()
#             self.auth_type = "Session"

#         self.auth_user.client = self.client
#         self.auth_user.on_start()

#     @task(3)
#     def get_profile(self):
#         """Delegate profile access to auth method"""
#         self.auth_user.get_profile()

#     @task(1)
#     def logout_and_login(self):
#         """Delegate logout/login to auth method"""
#         self.auth_user.logout_and_login()


if __name__ == "__main__":
    print(
        """
    AUTHENTICATION PERFORMANCE TESTING
    ==================================
    
    Currently configured to test: JWT Authentication Only
    
    To test different scenarios:
    1. Comment/uncomment the test classes above
    2. Only leave ONE test class uncommented
    
    Available tests:
    - JWTOnlyTest: Tests only JWT authentication
    - SessionOnlyTest: Tests only Session authentication  
    - MixedAuthTest: Tests both methods together
    
    Run command:
    locust -f tests/performance/locustfile.py --host=http://127.0.0.1:5001
    
    Then open: http://localhost:8089
    """
    )
