import random
import string
from locust import HttpUser, task, between


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


class JWTAuthUser(HttpUser):
    """Test JWT-based authentication performance"""

    wait_time = between(1, 3)  # Wait 1-3 seconds between requests

    def on_start(self):
        """Called when a user starts - registers and logs in"""
        self.user_data = generate_unique_user_data()
        self.access_token = None
        self.register_user()
        self.login_user()

    def register_user(self):
        """Register a new user"""
        with self.client.post(
            "/api/jwt/register",
            json=self.user_data,
            name="JWT Register",
            catch_response=True,
        ) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f"Registration failed: {response.status_code}")

    def login_user(self):
        """Login via JWT and store token"""
        login_data = {
            "identifier": self.user_data["email"],
            "password": self.user_data["password"],
        }

        with self.client.post(
            "/api/jwt/login",
            json=login_data,
            name="JWT Login",
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                if self.access_token:
                    response.success()
                else:
                    response.failure("No access token in response")
            else:
                response.failure(f"Login failed: {response.status_code}")

    @task(5)
    def get_profile(self):
        """Get profile using JWT token - most frequent operation"""
        if not self.access_token:
            return

        headers = {"Authorization": f"Bearer {self.access_token}"}

        with self.client.get(
            "/api/jwt/profile",
            headers=headers,
            name="JWT Get Profile",
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                # Token might be expired or invalid, try to re-login
                response.failure("Token expired or invalid")
                self.login_user()
            else:
                response.failure(f"Profile access failed: {response.status_code}")

    @task(1)
    def logout_and_login_cycle(self):
        """Occasionally logout and login again to test full cycle"""
        if not self.access_token:
            return

        # Logout
        headers = {"Authorization": f"Bearer {self.access_token}"}
        with self.client.delete(
            "/api/jwt/logout",
            headers=headers,
            name="JWT Logout",
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
                self.access_token = None
            else:
                response.failure(f"Logout failed: {response.status_code}")

        # Login again
        self.login_user()

    def on_stop(self):
        """Called when user stops - cleanup"""
        if self.access_token:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            self.client.delete("/api/jwt/logout", headers=headers, name="JWT Logout")


class JWTStressTest(HttpUser):
    """Stress test with rapid requests"""

    wait_time = between(0.1, 0.5)  # Very short wait time for stress testing

    def on_start(self):
        """Quick setup for stress testing"""
        self.user_data = generate_unique_user_data()
        self.access_token = None

        # Register and login
        self.client.post("/api/jwt/register", json=self.user_data)

        login_data = {
            "identifier": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post("/api/jwt/login", json=login_data)

        if response.status_code == 200:
            self.access_token = response.json().get("access_token")

    @task(10)
    def rapid_profile_access(self):
        """Rapid profile access for stress testing"""
        if not self.access_token:
            return

        headers = {"Authorization": f"Bearer {self.access_token}"}
        self.client.get(
            "/api/jwt/profile", headers=headers, name="Stress Profile Access"
        )


# Choose which test to run by commenting/uncommenting


# Normal load testing
class LoadTest(JWTAuthUser):
    """Normal load testing - recommended for general performance testing"""

    weight = 1





if __name__ == "__main__":
    print(
        """
    JWT AUTHENTICATION PERFORMANCE TESTING
    =====================================
    
    Available Test Modes:
    
    1. LoadTest (Active): 
       - Normal user behavior simulation
       - 1-3 second wait between requests
       - Mix of profile access and login/logout cycles
    
    2. StressTest (Commented): 
       - High-frequency requests
       - 0.1-0.5 second wait between requests
       - Rapid profile access
    
    To switch modes:
    - Comment/uncomment the test classes above
    
    Run Commands:
    
    Basic Test:
    locust -f test/locustfile.py --host=http://127.0.0.1:5000
    
    Headless Test (10 users, 2 spawn rate, 30 seconds):
    locust -f test/locustfile.py --host=http://127.0.0.1:5000 --users 10 --spawn-rate 2 --run-time 30s --headless
    
    Then open: http://localhost:8089 (for web UI)
    """
    )
