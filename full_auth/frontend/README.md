# Key Learnings
Building a simple authentication component taught me a lot about React so I document what I've learned along the way with some diagram and notes. I hope this is helpful.
- [Axios](#axios)
- [Context](#context)
- [Hooks](#hooks)

## Axios
### Explanation
- So your frontend needs to make some request from the client to the server. That's why we use Axios as a promise-based HTTP Client for the browser and `node.js`. 
### How to use axios
### Interceptors

## Context
### Explanation
-  `context` helps us define the state globally, meaning **letting the parent component pass on the information to any component below it** without passing the prop explicitly.
- Why is this useful? Because it addresses the problem of prop drilling. For example, user information like their authenticated token needs to be passed on to other tokens like dashboard, cards, etc., and any other components that are part of the protected resources.
- There are 3 steps to use `context` in React:
    1. **Create and export** a `Context`
    2. **Pass the context** to the `useContext(Context)` **hook** to read it in any child component, no matter how deep
    3. **Wrap** children into `<Context value={...}>` to provide it from a parent.
### Use Cases
- **Theming**: Switching between light mode and dark mode. This can be done by putting a context provider at the top of the app and use it in components that need to adjust the visual look.
- **Current account**: Components that need to know the *currently logged in user*. This is the use case that I'm using for this application
- **Routing**: Use context internally to hold the current route. 
- **Managing state**: Use a *reducer together with context* to manage complext state and pass it down to distant components.
### How to use context to pass down authentication information?
![context_auth](https://github.com/user-attachments/assets/dd33342e-5d5c-4e89-8faf-c48aba7c2b92)

## Hooks

## Resources
[1] https://react.dev/learn/passing-data-deeply-with-context

[2] https://axios-http.com/docs/intro