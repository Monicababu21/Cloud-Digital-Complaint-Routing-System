
function checkAuth(allowedRoles = []) {
    const token = localStorage.getItem('token');
    const userStr = localStorage.getItem('user');
    
    if (!token || !userStr) {
        window.location.href = '/index.html';
        return null;
    }
    
    const user = JSON.parse(userStr);
    
    if (allowedRoles.length > 0 && !allowedRoles.includes(user.role)) {
        let target = '/dashboard.html';
        if (user.role === 'admin') target = '/admin/dashboard.html';
        else if (user.role === 'staff') target = '/staff/dashboard.html';
        
        // Prevent infinite loop if already on the target page
        if (window.location.pathname !== target) {
            window.location.href = target;
        } else {
            // If we are on the target page but don't have the allowed role, the token data is invalid.
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/index.html';
        }
        return null;
    }
    
    return user;
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/index.html';
}

function setupNavbar(user) {
    const menu = document.getElementById('navbar-menu');
    if (!menu) return;
    
    let html = '';
    if (user.role === 'admin') {
        html += `<a href="/admin/dashboard.html">Dashboard</a>`;
        html += `<a href="/admin/complaints.html">Complaints</a>`;
        html += `<a href="/admin/departments.html">Departments</a>`;
        html += `<a href="/admin/users.html">Users</a>`;
    } else if (user.role === 'staff') {
        html += `<a href="/staff/dashboard.html">Dashboard</a>`;
        html += `<a href="/staff/complaints.html">Complaints</a>`;
    } else {
        html += `<a href="/dashboard.html">Dashboard</a>`;
        html += `<a href="/submit-complaint.html">Submit Complaint</a>`;
        html += `<a href="/complaints.html">My Complaints</a>`;
    }
    
    html += `<a href="/notifications.html">Notifications <span class="nav-badge" id="nav-notif-count">0</span></a>`;
    html += `<a href="#" onclick="logout(); return false;">Logout (${user.name})</a>`;
    menu.innerHTML = html;
    
    fetchUnreadNotifications();
}

async function fetchUnreadNotifications() {
    try {
        const notifs = await apiCall('/notifications');
        const count = notifs.filter(n => !n.is_read).length;
        const badge = document.getElementById('nav-notif-count');
        if (badge) {
            badge.textContent = count;
            badge.style.display = count > 0 ? 'inline' : 'none';
        }
    } catch(e) {}
}
