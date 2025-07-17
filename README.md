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

<img width="888" height="623" alt="Screenshot 2025-07-17 at 8 06 22 PM" src="https://github.com/user-attachments/assets/7a8da77b-5227-4387-a41a-dede3938e15f" />


### Sign Up

Standard Registration

- [x] Use first/last names, username, email, and password
- [x] Confirm account via email

### OAuth Registration

- [x] Use a Google Account to sign up

### Standard Login

- [x] Use an identifier (either username or email) and password
- [x] If the user forgot their password, there should be an option for them to reset their password by:
  - [x] Sending a link to reset their password to their registered email
  - [x] User clicks the link and is redirected to the password reset page
  - [x] They enter their new password
  - [x] Log in again

### OAuth Login

- [x] Use a Google Account sign in

### Profile

- [x] Users should be able to change their username/email, or password
- [x] Users should be able to delete their accounts

## Session-based Authentication

### Explanation

First of all, HTTP is a stateless protocol, which means the client or the server does not keep track of the subsequent requests - each of them is treated as an independent one. Sessions allow the server to associate some information with a client, hence making it easier to retrieve the information for a request. The key difference compared to JWT is that session-based auth has storage both on the server and client side. On the client side, the cookie is stored in session/local storage, and on the server side, it is stored in memory.

Because sessions are stored on the server, it gives more control to the administrators to invalidate a session ID. Also, note that because we are using cookies, we need to pay attention to CORS to allow communication between two different domains.

![image](https://github.com/user-attachments/assets/0efd95ac-9116-4019-a5b4-7982c959ef47)

### Configuration & Setup

0. Create a virtual environment inside the `session_auth` using `python3 -m venv .venv` and activate it `. .venv/bin/activate`
1. Create a `.env` file with the following environment variables

```
# Flask Environment
FLASK_ENV=development

# Development variables
DEV_DATABASE_URI=sqlite:///development.db
DEV_SECRET_KEY={your-dev-secret-key}

# Production variables
PROD_DATABASE_URI=sqlite:///production.db
PROD_SECRET_KEY={your-production-secret-key}
```

## JSON Web Token Authentication

### Explanation

JSON Web Tokens Components. The format of a JWT is xxxxx.yyyyy.zzzzz, where each part is separated by a dot and represents the header, payload, and signature, respectively.
JSON Web Token is a standard that defines a way for parties to transmit data. The security part comes from the digital signature - a secret with the HMAC algorithm (Hash-based Message Authentication Code) or a public/private key pair. So basically, you can also encrypt the token such that the claims are hidden. JWT is used for the following purposes:

- **Authorization**: User logged in → request includes JWT → user can access routes, services, and resources associated with that token. I’ve just learned that Single Sign On (SSO) uses JWT! This is when I sign in to my Google account on my laptop, and then I will be automatically logged in to Google’s services like YouTube or Gmail.
- **Information Exchange**: Secure information transmission because it makes sure that the senders are who they say they are, thanks to the keys.

![image](https://github.com/user-attachments/assets/775a257c-1850-4670-b5d0-94d17ddc3a28)

### Configuration & Setup

0. Create a virtual environment inside the `jwt_auth` using `python3 -m venv .venv` and activate it `. .venv/bin/activate`
1. Create a `.env` file with the following environment variables

```
# Flask Environment
FLASK_ENV=development

# Development variables
DEV_DATABASE_URI=sqlite:///development.db
DEV_JWT_SECRET_KEY={your-dev-secret-key}
DEV_REDIS_URL=redis://localhost:6379/1

# Production variables
PROD_DATABASE_URI=sqlite:///production.db
PROD_JWT_SECRET_KEY={your-production-secret-key}
PROD_REDIS_URL=redis://localhost:6379/0

# Default Redis (fallback)
REDIS_URL=redis://localhost:6379/0
```

2. In order to log out the user, we need to initialize a connection to a Redis server running on - you should set the REDIS_URL in your `.env` file:

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

3. To run the app in development mode, follow the commands:

```
export FLASK_ENV=development
flask --app run init-db
flask --app run migrate-db -m "Initial migration"
flask --app run upgrade-db
flask --app run show-db-info

python3 run.py
```

4. To run the app in testing mode, follow the commands:

```
export FLASK_ENV=testing
python3 run.py
```

## OAuth Authentication

# Performance Testing

When I did some research online, there was often this statement saying that JWT is more scalable compared to session-based auth, while the latter offers more control. Then, one question arose: "How can I empirically test if this statement is true or not?" And then I learned about Locust - a load testing tool. To run the locust file in development mode:

```
cd tests
locust -f locustfile.py --host=http://127.0.0.1:5000
```

The results from two different setups (number of users 100 vs. 500 with the same ramp-up rate) seemed a bit counterintuitive at first because my expectation was that JWT should be more efficient, both in time and space, compared to session-based. It turned out not to be the case from the experiments (check out the statistics table below). In terms of average size (bytes) and response, session-based authentication turned out to be better! There are a couple of reasons I think why this is the case:

- Only one Flask server setup makes it easier for session-based auth because there is no need for token parsing or JWT decoding/validation overhead or querying from Redis.
- The session data is stored in local memory, so it makes the lookup faster in a single-server environment.

I did some research online and found some helpful Reddit and StackOverflow threads discussing the benefits of using **JWT in a distributed and microservice system** when you want to scale your software horizontally, because there is no need for a shared session store. The key takeaway I got from running this experiment is that, when someone says something is more scalable, we really need to understand what "scalable" exactly means, in which context and applicable to which architecture.

### Session Authentication Load Testing (Number of Users = 100 - Peak Concurrency, Ramp up = 10, 2 Minutes)

<img width="1134" alt="Screenshot 2025-07-03 at 9 12 35 AM" src="https://github.com/user-attachments/assets/c7e17f8f-3b46-44a3-a66f-d713962318fe" />

### JWT Authentication Load Testing (Number of Users = 100 - Peak Concurrency, Ramp up = 10, 2 Minutes)

<img width="1134" alt="Screenshot 2025-07-03 at 9 23 16 AM" src="https://github.com/user-attachments/assets/e4ccaa19-b99e-4fa5-963b-9d7d0e283313" />

### JWT Authentication Load Testing (Number of Users = 500 - Peak Concurrency, Ramp up = 10, 2 Minutes)

<img width="1141" alt="Screenshot 2025-07-03 at 9 34 52 AM" src="https://github.com/user-attachments/assets/fc898429-4622-4b98-96c2-656d8b72cbb9" />

### Session Authentication Load Testing (Number of Users = 500 - Peak Concurrency, Ramp up = 10, 2 Minutes)

<img width="1136" alt="Screenshot 2025-07-03 at 9 38 06 AM" src="https://github.com/user-attachments/assets/8f470720-2e37-42df-bebd-ed069dc502e2" />

# References

[1] https://jwt.io/introduction

[2] https://auth0.com/docs/secure/tokens/json-web-tokens

[3] https://roadmap.sh/guides/session-based-authentication

[4] https://roadmap.sh/guides/session-authentication

[5] https://auth0.com/intro-to-iam/what-is-oauth-2

[6] https://www.reddit.com/r/node/comments/1aox0au/whats_the_ultimate_resource_for_jwt_vs_session/

[7] https://stackoverflow.com/questions/43452896/authentication-jwt-usage-vs-session

[8] http://cryto.net/~joepie91/blog/2016/06/13/stop-using-jwt-for-sessions/

[9] https://github.com/authlib/demo-oauth-client/tree/master/flask-google-login
