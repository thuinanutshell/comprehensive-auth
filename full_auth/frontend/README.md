# Key Learnings
- [Context](#context)
- [Hooks](#hooks)

## Context
### Explanation
-  `context` helps us define the state globally, meaning **letting the parent component pass on the information to any component below it** without passing the prop explicitly.
- Why is this useful? Because it addresses the problem of prop drilling. For example, user information like their authenticated token needs to be passed on to other tokens like dashboard, cards, etc., and any other components that are part of the protected resources.
- There are 3 steps to use `context` in React:
    1. **Create** a context
    2. **Use** that context from the component that needs the data (child components)
    3. **Provide** that context from the component that specifies the data (parent)
### How to use context to pass down authentication information?
![context_auth](https://github.com/user-attachments/assets/dd33342e-5d5c-4e89-8faf-c48aba7c2b92)

## Hooks

## Resources
[1] https://react.dev/learn/passing-data-deeply-with-context
