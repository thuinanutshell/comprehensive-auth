import axios from 'axios';

const BASE_URL = import.meta.env.VITE_BACKEND_BASE_URL || 'http://localhost:5000/api/auth'
axios.defaults.baseURL = BASE_URL

// Configure axios to add token to every request before it is sent
axios.interceptors.request.use(config => {
    const token = localStorage.getItem("token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
})

async function register(credentials) {
    try {
        const response = await axios.post('/register', credentials);
        console.log(response)
        return response.data
    } catch (error) {
        console.error(error);
        throw error;
    }
}

async function login(credentials) {
    try {
        const response = await axios.post('/login', credentials);
        console.log(response)
        return response.data
    } catch (error) {
        console.error(error);
        throw error;
    }
}

async function logout() {
    try {
        const response = await axios.delete('/logout');
        return response.data;
    } catch (error) {
        console.error(error);
        throw error;
    }
}

async function verify_token(token) {
    try {
        const response = await axios.post(`/verify/${token}`)
        console.log(response)
        return response.data;
    } catch (error) {
        console.error(error);
        throw error;
    }
}

// OAuth functions - these should redirect the browser, not make AJAX calls
function login_oauth() {
    window.location.href = `${BASE_URL}/login/oauth`;
}

async function check_oauth_status() {
    try {
        const response = await axios.get('/oauth2callback')
        console.log(response)
        return response.data;
    } catch (error) {
        console.error(error);
        throw error;
    }
}

async function protected_route() {
    try {
        const response = await axios.get('/protected');
        console.log(response)
        return response.data;
    } catch (error) {
        console.error(error);
        throw error;
    }
}

async function update_profile(profileData) {
    try {
        const response = await axios.patch('/profile', profileData);
        console.log(response)
        return response.data
    } catch (error) {
        console.error(error);
        throw error;
    }
}

async function delete_profile() {
    try {
        const response = await axios.delete('/profile')
        console.log(response)
        return response.data
    } catch (error) {
        console.error(error);
        throw error;
    }
}

export {
    check_oauth_status,
    delete_profile,
    login,
    login_oauth,
    logout,
    protected_route,
    register,
    update_profile,
    verify_token
};

