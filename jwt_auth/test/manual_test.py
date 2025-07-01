import requests
import json
from app import create_app

BASE_URL = "http://127.0.0.1:5001"

# Create app and initialize database
app = create_app(config="testing")


def test_jwt_register_success():
    """Test JWT authentication registration"""
    print("🔄 Testing JWT Registration...")
    try:
        data = {
            "first_name": "test",
            "last_name": "user",
            "username": "jwtuser",
            "email": "jwtuser@gmail.com",
            "password": "testuser123!",
        }
        response = requests.post(f"{BASE_URL}/api/jwt/register", json=data)

        if response.status_code == 201:
            print("✅ JWT Register: SUCCESS")
            return True
        else:
            print(f"❌ JWT Register: FAILED - Status {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ JWT Register: FAILED - Server not running")
        return False
    except Exception as e:
        print(f"❌ JWT Register: ERROR - {e}")
        return False


def test_jwt_login_success():
    """Test JWT authentication login"""
    print("🔄 Testing JWT Login...")
    try:
        data = {"identifier": "jwtuser@gmail.com", "password": "testuser123!"}
        response = requests.post(f"{BASE_URL}/api/jwt/login", json=data)

        if response.status_code == 200:
            token = response.json().get("access_token")
            if token:
                print("✅ JWT Login: SUCCESS")
                return token
            else:
                print("❌ JWT Login: FAILED - No token in response")
                return None
        else:
            print(f"❌ JWT Login: FAILED - Status {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except Exception as e:
        print(f"❌ JWT Login: ERROR - {e}")
        return None


def test_jwt_profile_access(token):
    """Test JWT authentication profile access"""
    print("🔄 Testing JWT Profile Access...")
    if not token:
        print("❌ JWT Profile: FAILED - No token provided")
        return False

    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/jwt/profile", headers=headers)

        if response.status_code == 200:
            print("✅ JWT Profile: SUCCESS")
            profile_data = response.json()
            print(f"   User: {profile_data.get('data', {}).get('Username', 'Unknown')}")
            return True
        else:
            print(f"❌ JWT Profile: FAILED - Status {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ JWT Profile: ERROR - {e}")
        return False


def test_jwt_logout(token):
    """Test JWT authentication logout"""
    print("🔄 Testing JWT Logout...")
    if not token:
        print("❌ JWT Logout: FAILED - No token provided")
        return False

    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{BASE_URL}/api/jwt/logout", headers=headers)

        if response.status_code == 200:
            print("✅ JWT Logout: SUCCESS")
            return True
        else:
            print(f"❌ JWT Logout: FAILED - Status {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ JWT Logout: ERROR - {e}")
        return False


def main():
    """Main function to run all authentication tests"""
    test_jwt_register_success()
    test_jwt_login_success()
    test_jwt_profile_success()
    test_jwt_logout()


if __name__ == "__main__":
    main()
