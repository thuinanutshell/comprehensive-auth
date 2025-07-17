import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function LoginForm() {
    // Set the initial data for the fields and the function to update them
    const [data, setData] = useState({
        username: '',
        email: '',
        password: '',
    })

    // Set the initial navigate variable
    const navigate = useNavigate()

    // Set the function to update the data based on the event
    const handleChange = (e) => {
        setData({
            ...data,
            [e.target.name]: e.target.value
        })
    }

    // Define a function for what happens after the user submits the data
    const handleSubmit = (e) => {
        e.preventDefault();
        // The user should be navigated to the homepage if they are authenticated
        navigate('/dashboard')
    }

    return (
        <form onSubmit={handleSubmit}>
            <input onChange={handleChange} required />Username:
            <input onChange={handleChange} required />Email:
            <input onChange={handleChange} required />Password:
            <button>Login</button>
        </form>
    )

} 