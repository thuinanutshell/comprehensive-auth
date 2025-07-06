# Key Learnings

## What exactly is context?
-  `context` helps us define the state globally, meaning **letting the parent component pass on the information to any component below it** without passing the prop explicitly.
- Why is this useful? Because it addresses the problem of prop drilling. For example, user information like their authenticated token needs to be passed on to other tokens like dashboard, cards, etc. - any other components that are part of the protected resources.
- There are 3 steps to use `context` in React:
    1. **Create** a context
    2. **Use** that context from the component that needs the data (children components)
    3. **Provide** that context from the component that specifies the data (parent)

## Resources
[1] https://react.dev/learn/passing-data-deeply-with-context