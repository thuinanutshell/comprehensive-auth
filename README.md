# How to Build a Comprehensive Authentication Feature Using Different Methods (JWT, Session-based & OAuth)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Locust](https://img.shields.io/badge/Locust-1A1A1A?style=for-the-badge&logo=locust&logoColor=green)
![Pytest](https://img.shields.io/badge/PYTEST-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)


## Table of Contents
- [Features](#features)
- [Session-based Authentication](#session-based-authentication)
- [JSON Web Token Authentication](#json-web-token-authentication)
- [OAuth Authentication](#oauth-authentication)
- [Performance Testing](#performance-testing)

I realized how much I used to struggle in developing the authentication feature for my applications. Such a simple feature caused a lot of headaches, and I am not ashamed to admit that. Because authentication is so integral in many applications. I am curious about how I could create one similar to that. A comprehensive authentication feature will need to have the following functionalities.

# Features
###  Sign Up
Standard Registration
- [ ] Use first/last names, username, email, and password
- [ ] Confirm account via email
### OAuth Registration
- [ ] Use a Google Account, LinkedIn, GitHub, etc., to sign up
### Standard Login
- [ ] Use an identifier (either username or email) and password
- [ ] If the user forgot their password, there should be an option for them to reset their password by:
  - [ ] Sending a link to reset their password to their registered email
  - [ ] User clicks the link and is redirected to the password reset page
  - [ ] They enter their new password
  - [ ] Log in again
### OAuth Login
- [ ] Use a Google Account, LinkedIn, GitHub, etc., to sign in

### Profile
- [ ] Users should be able to change their username/email, or password
- [ ] Users should be able to delete their accounts
  
## Session-based Authentication
First of all, HTTP is a stateless protocol, which means the client or the server does not keep track of the subsequent requests - each of them is treated as an independent one. Sessions allow the server to associate some information with a client, hence making it easier to retrieve the information for a request. The key difference compared to JWT is that session-based auth has storage both on the server and client side. On the client side, the cookie is stored in session/local storage, and on the server side, it is stored in memory.

Because sessions are stored on the server, it gives more control to the administrators to invalidate a session ID. Also, note that because we are using cookies, we need to pay attention to CORS to allow communication between two different domains.

![image](https://github.com/user-attachments/assets/0efd95ac-9116-4019-a5b4-7982c959ef47)


## JSON Web Token Authentication
JSON Web Tokens Components. The format of a JWT is xxxxx.yyyyy.zzzzz, where each part is separated by a dot and represents the header, payload, and signature, respectively.
JSON Web Token is a standard that defines a way for parties to transmit data. The security part comes from the digital signature - a secret with the HMAC algorithm (Hash-based Message Authentication Code) or a public/private key pair. So basically, you can also encrypt the token such that the claims are hidden. JWT is used for the following purposes:

- **Authorization**: User logged in → request includes JWT → user can access routes, services, and resources associated with that token. I’ve just learned that Single Sign On (SSO) uses JWT! This is when I sign in to my Google account on my laptop, and then I will be automatically logged in to Google’s services like YouTube or Gmail.
- **Information Exchange**: Secure information transmission because it makes sure that the senders are who they say they are, thanks to the keys.
  
![image](https://github.com/user-attachments/assets/775a257c-1850-4670-b5d0-94d17ddc3a28)


In order to log out the user, we need to initialize a connection to a Redis server running on - you should set the REDIS_URL in your `.env` file:
```python
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
```
- `host="localhost"`: your local machine
- `port=6379`: the default Redis port
- `db=0`: the default Redis database index
- `decode_responses=True`: ensures Redis returns strings (not bytes)
When users log out or a token needs to be invalidated before it expires, you can't remove or "cancel" a JWT since it's stateless. So, a common solution is to store a "blocklist" of token identifiers (like the jti claim) in Redis, so your app can check against this list when validating tokens.

## OAuth Authentication

# Performance Testing
When I did some research online, there was often this statement saying that JWT is more scalable compared to session-based auth, while the latter offers more control. Then, one question arose: "How can I empirically test if this statement is true or not?" And then I learned about Locust - a load testing tool. Below is the test setup
# References
[1] https://jwt.io/introduction

[2] https://auth0.com/docs/secure/tokens/json-web-tokens

[3] https://roadmap.sh/guides/session-based-authentication

[4] https://roadmap.sh/guides/session-authentication

[5] https://auth0.com/intro-to-iam/what-is-oauth-2




