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
        "password": "StrongPass123!",
    }


class SessionAuthUser(HttpUser):
    """Test session-based authentication performance"""

    wait_time = between(1, 3)  # Wait 1-3 seconds between requests

    def on_start(self):
        """Called when a user starts - registers and logs in"""
        self.user_data = generate_unique_user_data()
        self.register_user()
        self.login_user()

    def register_user(self):
        """Register a new user"""
        with self.client.post(
            "/api/session/register",
            json=self.user_data,
            name="Session Register",
            catch_response=True,
        ) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f"Registration failed: {response.status_code}")

    def login_user(self):
        """Login via session cookies"""
        login_data = {
            "identifier": self.user_data["email"],
            "password": self.user_data["password"],
        }

        with self.client.post(
            "/api/session/login",
            json=login_data,
            name="Session Login",
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Login failed: {response.status_code}")

    @task(5)
    def get_profile(self):
        """Get profile using session cookie - most frequent operation"""
        with self.client.get(
            "/api/session/profile",
            name="Session Get Profile",
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code in [401, 302]:
                self.login_user()
            else:
                response.failure(f"Profile access failed: {response.status_code}")

    @task(1)
    def logout_and_login_cycle(self):
        """Occasionally logout and login again to test full cycle"""
        # Logout
        with self.client.post(
            "/api/session/logout",
            name="Session Logout",
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Logout failed: {response.status_code}")

        # Login again
        self.login_user()

    def on_stop(self):
        """Called when user stops - cleanup"""
        self.client.post("/api/session/logout", name="Session Logout")


class SessionStressTest(HttpUser):
    """Stress test with rapid requests"""

    wait_time = between(0.1, 0.5)  # Very short wait time for stress testing

    def on_start(self):
        """Quick setup for stress testing"""
        self.user_data = generate_unique_user_data()

        self.client.post(
            "/api/session/register", json=self.user_data, name="Session Register"
        )

        login_data = {
            "identifier": self.user_data["email"],
            "password": self.user_data["password"],
        }
        self.client.post("/api/session/login", json=login_data, name="Session Login")

    @task(10)
    def rapid_profile_access(self):
        """Rapid profile access for stress testing"""
        self.client.get("/api/session/profile", name="Session Get Profile")


# Normal load testing
class LoadTest(SessionAuthUser):
    """Normal load testing - recommended for general performance testing"""

    weight = 1


class StressTest(SessionStressTest):
    """Stress testing - uncomment to enable"""

    weight = 1


if __name__ == "__main__":
    print(
        """
    SESSION AUTHENTICATION PERFORMANCE TESTING
    =========================================
    
    Available Test Modes:
    
    1. LoadTest (Active): 
       - Normal user behavior simulation
       - 1-3 second wait between requests
       - Mix of profile access and login/logout cycles
    
    2. StressTest (Disabled): 
       - High-frequency requests
       - 0.1-0.5 second wait between requests
       - Rapid profile access
       - Uncomment StressTest class above to enable
    
    Run Commands:
    
    Basic Test:
    locust -f locustfile.py --host=http://127.0.0.1:5000
    
    Headless Test (10 users, 2 spawn rate, 30 seconds):
    locust -f locustfile.py --host=http://127.0.0.1:5000 --users 10 --spawn-rate 2 --run-time 30s --headless
    
    Then open: http://localhost:8089 (for web UI)
    """
    )
