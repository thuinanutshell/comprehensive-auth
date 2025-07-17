import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function RegisterForm() {
    const [data, setData] = useState({
        first_name: '',
        last_name: '',
        username: '',
        email: '',
        password: ''
    })
    const navigate = useNavigate()

    const handleChange = (e) => {
        setData({
            ...data,
            [e.target.name]: e.target.value
        })
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        navigate('/dashboard')
    }

    return (
        <form onSubmit={handleSubmit}>
            <input onChange={handleChange}/>First Name:
            <input onChange={handleChange}/>Last Name:
            <input onChange={handleChange}/>Username: 
            <input onChange={handleChange}/>Email: 
            <input onChange={handleChange}/>Password: 
            <button>Register</button>
        </form>
    )
}