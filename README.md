# How to Build a Comprehensive Authentication Feature

I realized how much I used to struggle in developing the authentication feature for my applications. Such a simple feature caused a lot of headaches, and I am not ashamed to admit that. Because authentication is so integral in many applications. I am curious about how I could create one similar to that. A comprehensive authentication feature will need to have these functionalities:

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
- Use a Google Account, LinkedIn, GitHub, etc., to sign up

## Profile
- The user should be able to change their username/email or password
