# How to Build a Comprehensive Authentication Feature Using Different Methods
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Locust](https://img.shields.io/badge/Locust-1A1A1A?style=for-the-badge&logo=locust&logoColor=green)

## Table of Contents
- [Features](#features)
- [Session-based Authentication](#session-based-authentication)
- [JSON Web Token Authentication](#json-web-token-authentication)
- [OAuth Authentication](#oauth-authentication)
- [Performance Testing](#performance-testing)

I realized how much I used to struggle in developing the authentication feature for my applications. Such a simple feature caused a lot of headaches, and I am not ashamed to admit that. Because authentication is so integral in many applications. I am curious about how I could create one similar to that. A comprehensive authentication feature will need to have the following functionalities.

# Features
## Sign Up
### Standard Registration
- Use first/last names, username, email, and password
- Confirm account via email
### OAuth Registration
- Use a Google Account, LinkedIn, GitHub, etc., to sign up

## Log In
### Standard Login
- Use an identifier (either username or email) and password
- If the user forgot their password, there should be an option for them to reset their password by:
  - Sending a link to reset their password to their registered email
  - User clicks the link and is redirected to the password reset page
  - They enter their new password
  - Log in again

### OAuth Login
- Use a Google Account, LinkedIn, GitHub, etc., to sign in

## Profile
- The user should be able to change their username/email, or password
  
## Session-based Authentication
## JSON Web Token Authentication
## OAuth Authentication

# Performance Testing
