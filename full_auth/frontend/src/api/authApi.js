import axios from 'axios';

const BASE_URL = import.meta.env.VITE_BACKEND_BASE_URL || 'http://localhost:5000'
axios.defaults.baseURL = BASE_URL
axios.interceptors.request.use(config => {
    const token = localStorage.getItem("token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
})


async function register(credentials) {
    try {
        const response = await axios.post('/auth/register', credentials);
        console.log(response)
        return response.data
    } catch (error) {
        console.error(error);
    }
}

async function login(credentials) {
    try {
        const response = await axios.post('/auth/login', credentials);
        console.log(response)
        return response.data
    } catch (error) {
        console.error(error);
    }
}

async function logout(token) {
    try {
        const response = await axios.delete('/auth/logout', {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        return response.data;
    } catch (error) {
        console.error(error);
    }
}

export { login, logout, register };
