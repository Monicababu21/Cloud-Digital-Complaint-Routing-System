
const API_URL = 'http://localhost:5000/api';

function getHeaders() {
    const token = localStorage.getItem('token');
    return {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
    };
}

async function apiCall(endpoint, method = 'GET', body = null) {
    try {
        const options = { method, headers: getHeaders() };
        if (body) options.body = JSON.stringify(body);
        
        const res = await fetch(`${API_URL}${endpoint}`, options);
        const data = await res.json();
        
        if (!res.ok) {
            if ((res.status === 401 || res.status === 403) && !endpoint.includes('/auth/login')) {
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                window.location.href = '/index.html';
            }
            throw new Error(data.message || 'API Error');
        }
        return data;
    } catch (e) {
        throw e;
    }
}
