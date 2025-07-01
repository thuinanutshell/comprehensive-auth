import requests
import json

BASE_URL = "http://127.0.0.1:5001"


def test_session_register_success():
    """Test session authentication registration"""
    print("🔄 Testing Session Registration...")
    try:
        data = {
            "first_name": "test",
            "last_name": "user",
            "username": "sessionuser",
            "email": "sessionuser@gmail.com",
            "password": "testuser123!",
        }
        response = requests.post(f"{BASE_URL}/api/session/register", json=data)

        if response.status_code == 201:
            print("✅ Session Register: SUCCESS")
            return True
        else:
            print(f"❌ Session Register: FAILED - Status {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Session Register: FAILED - Server not running")
        return False
    except Exception as e:
        print(f"❌ Session Register: ERROR - {e}")
        return False


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


def test_session_login_success():
    """Test session authentication login"""
    print("🔄 Testing Session Login...")
    try:
        session = requests.Session()
        data = {"identifier": "sessionuser@gmail.com", "password": "testuser123!"}
        response = session.post(f"{BASE_URL}/api/session/login", json=data)

        if response.status_code == 200:
            print("✅ Session Login: SUCCESS")
            return session
        else:
            print(f"❌ Session Login: FAILED - Status {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Session Login: ERROR - {e}")
        return None


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


def test_session_profile_access(session):
    """Test session authentication profile access"""
    print("🔄 Testing Session Profile Access...")
    if not session:
        print("❌ Session Profile: FAILED - No session provided")
        return False

    try:
        response = session.get(f"{BASE_URL}/api/session/profile")

        if response.status_code == 200:
            print("✅ Session Profile: SUCCESS")
            profile_data = response.json()
            print(f"   User: {profile_data.get('data', {}).get('Username', 'Unknown')}")
            return True
        else:
            print(f"❌ Session Profile: FAILED - Status {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Session Profile: ERROR - {e}")
        return False


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


def test_session_logout(session):
    """Test session authentication logout"""
    print("🔄 Testing Session Logout...")
    if not session:
        print("❌ Session Logout: FAILED - No session provided")
        return False

    try:
        response = session.post(f"{BASE_URL}/api/session/logout")

        if response.status_code == 200:
            print("✅ Session Logout: SUCCESS")
            return True
        else:
            print(f"❌ Session Logout: FAILED - Status {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Session Logout: ERROR - {e}")
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


def compare_auth_systems():
    """Compare session vs JWT authentication side by side"""
    print("\n" + "=" * 60)
    print("COMPARING AUTHENTICATION SYSTEMS")
    print("=" * 60)

    results = {
        "session": {
            "register": False,
            "login": False,
            "profile": False,
            "logout": False,
        },
        "jwt": {"register": False, "login": False, "profile": False, "logout": False},
    }

    # Test Session Auth Flow
    print(f"\n{'SESSION AUTHENTICATION':^30}")
    print("-" * 30)

    results["session"]["register"] = test_session_register_success()
    if results["session"]["register"]:
        session = test_session_login_success()
        if session:
            results["session"]["login"] = True
            results["session"]["profile"] = test_session_profile_access(session)
            results["session"]["logout"] = test_session_logout(session)

    # Test JWT Auth Flow
    print(f"\n{'JWT AUTHENTICATION':^30}")
    print("-" * 30)

    results["jwt"]["register"] = test_jwt_register_success()
    if results["jwt"]["register"]:
        token = test_jwt_login_success()
        if token:
            results["jwt"]["login"] = True
            results["jwt"]["profile"] = test_jwt_profile_access(token)
            results["jwt"]["logout"] = test_jwt_logout(token)

    # Print Comparison Summary
    print(f"\n{'RESULTS SUMMARY':^60}")
    print("=" * 60)
    print(f"{'Operation':<15} {'Session':<15} {'JWT':<15} {'Match':<15}")
    print("-" * 60)

    for operation in ["register", "login", "profile", "logout"]:
        session_result = "✅ PASS" if results["session"][operation] else "❌ FAIL"
        jwt_result = "✅ PASS" if results["jwt"][operation] else "❌ FAIL"
        match = (
            "✅ YES"
            if results["session"][operation] == results["jwt"][operation]
            else "❌ NO"
        )

        print(
            f"{operation.title():<15} {session_result:<15} {jwt_result:<15} {match:<15}"
        )

    # Overall Assessment
    session_total = sum(results["session"].values())
    jwt_total = sum(results["jwt"].values())

    print(f"\n{'OVERALL ASSESSMENT':^60}")
    print("=" * 60)
    print(f"Session Auth: {session_total}/4 tests passed")
    print(f"JWT Auth: {jwt_total}/4 tests passed")

    if session_total == jwt_total == 4:
        print("🎉 Both authentication systems are working perfectly!")
    elif session_total == jwt_total:
        print("⚠️  Both systems have the same issues - check server setup")
    else:
        print(
            "⚠️  Authentication systems have different behaviors - investigate differences"
        )

    return results


def main():
    """Main function to run all authentication tests"""
    print("🚀 STARTING AUTHENTICATION SYSTEM TESTS")
    print("=" * 60)
    print(f"Testing against: {BASE_URL}")
    print("Make sure your Flask server is running!")
    print("=" * 60)

    # Run comparison tests
    results = compare_auth_systems()

    print(f"\n{'TEST COMPLETE':^60}")
    print("=" * 60)

    return results


if __name__ == "__main__":
    main()
