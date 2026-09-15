import os

base_dir = "c:/Users/monica/OneDrive/Documents/CLOUD/Cloud-Digital-Complaint-Routing-System"

frontend_files = {
    "frontend/css/style.css": """
:root {
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --secondary: #64748b;
    --success: #22c55e;
    --warning: #eab308;
    --danger: #ef4444;
    --background: #f8fafc;
    --surface: #ffffff;
    --text: #0f172a;
    --text-muted: #64748b;
    --border: #e2e8f0;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', system-ui, sans-serif; background: var(--background); color: var(--text); line-height: 1.5; }
a { text-decoration: none; color: var(--primary); }
ul { list-style: none; }

/* Navbar */
.navbar { display: flex; justify-content: space-between; align-items: center; padding: 1rem 2rem; background: var(--surface); box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.navbar-brand { font-size: 1.25rem; font-weight: bold; color: var(--primary); }
.navbar-menu { display: flex; gap: 1.5rem; align-items: center; }
.navbar-menu a { color: var(--text); font-weight: 500; }
.navbar-menu a:hover { color: var(--primary); }
.nav-badge { background: var(--danger); color: white; border-radius: 9999px; padding: 0.1rem 0.5rem; font-size: 0.75rem; margin-left: 0.25rem; }

/* Layout */
.container { max-width: 1200px; margin: 2rem auto; padding: 0 1rem; }
.card { background: var(--surface); border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 1.5rem; margin-bottom: 1.5rem; }

/* Forms */
.form-group { margin-bottom: 1rem; }
label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
input, select, textarea { width: 100%; padding: 0.5rem; border: 1px solid var(--border); border-radius: 0.25rem; font-family: inherit; }
.btn { display: inline-block; padding: 0.5rem 1rem; border: none; border-radius: 0.25rem; cursor: pointer; font-weight: 500; transition: opacity 0.2s; text-align: center; }
.btn:hover { opacity: 0.9; }
.btn-primary { background: var(--primary); color: white; }
.btn-success { background: var(--success); color: white; }

/* Tables */
table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
th, td { padding: 0.75rem; text-align: left; border-bottom: 1px solid var(--border); }
th { font-weight: 600; color: var(--text-muted); }

/* Badges */
.badge { padding: 0.25rem 0.5rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
.badge-Low { background: #e0f2fe; color: #0284c7; }
.badge-Medium { background: #fef08a; color: #854d0e; }
.badge-High { background: #fed7aa; color: #c2410c; }
.badge-Urgent { background: #fecaca; color: #b91c1c; }

.badge-Pending { background: #f1f5f9; color: #475569; }
.badge-Routed { background: #e0e7ff; color: #3730a3; }
.badge-Assigned { background: #dbeafe; color: #1e40af; }
.badge-InProgress { background: #fef9c3; color: #854d0e; }
.badge-Resolved { background: #dcfce7; color: #166534; }
.badge-Rejected { background: #fee2e2; color: #991b1b; }

/* Dashboard Cards */
.grid-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
.stat-card { background: var(--surface); padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); text-align: center; }
.stat-card h3 { color: var(--text-muted); font-size: 0.875rem; margin-bottom: 0.5rem; }
.stat-card .value { font-size: 2rem; font-weight: bold; color: var(--primary); }

/* Alerts */
.alert { padding: 1rem; border-radius: 0.25rem; margin-bottom: 1rem; display: none; }
.alert-error { background: #fee2e2; color: #991b1b; border: 1px solid #f87171; }
.alert-success { background: #dcfce7; color: #166534; border: 1px solid #4ade80; }

.timeline { margin: 2rem 0; display: flex; justify-content: space-between; align-items: center; position: relative; }
.timeline::before { content: ''; position: absolute; top: 50%; left: 0; right: 0; height: 2px; background: var(--border); z-index: 1; }
.timeline-step { position: relative; z-index: 2; background: var(--surface); padding: 0.5rem 1rem; border-radius: 9999px; border: 2px solid var(--border); color: var(--text-muted); font-weight: 500; font-size: 0.875rem; }
.timeline-step.active { border-color: var(--primary); color: var(--primary); font-weight: bold; }
.timeline-step.completed { background: var(--primary); border-color: var(--primary); color: white; }

.auth-container { max-width: 400px; margin: 4rem auto; }
""",
    "frontend/js/api.js": """
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
            if (res.status === 401 || res.status === 403) {
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
""",
    "frontend/js/auth.js": """
function checkAuth(allowedRoles = []) {
    const token = localStorage.getItem('token');
    const userStr = localStorage.getItem('user');
    
    if (!token || !userStr) {
        window.location.href = '/index.html';
        return null;
    }
    
    const user = JSON.parse(userStr);
    
    if (allowedRoles.length > 0 && !allowedRoles.includes(user.role)) {
        if (user.role === 'admin') window.location.href = '/admin/dashboard.html';
        else if (user.role === 'staff') window.location.href = '/staff/dashboard.html';
        else window.location.href = '/dashboard.html';
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
""",
    "frontend/index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login - Complaint Routing System</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <div class="auth-container card">
        <h2 style="text-align: center; margin-bottom: 1.5rem; color: var(--primary)">Digital Complaint System</h2>
        <div id="alertBox" class="alert"></div>
        <form id="loginForm">
            <div class="form-group">
                <label>Email</label>
                <input type="email" id="email" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" id="password" required>
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%">Login</button>
        </form>
        <p style="text-align: center; margin-top: 1rem">
            Don't have an account? <a href="/signup.html">Sign up</a>
        </p>
    </div>

    <script src="/js/api.js"></script>
    <script>
        if (localStorage.getItem('token')) {
            const user = JSON.parse(localStorage.getItem('user'));
            if(user.role === 'admin') window.location.href = '/admin/dashboard.html';
            else if(user.role === 'staff') window.location.href = '/staff/dashboard.html';
            else window.location.href = '/dashboard.html';
        }

        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const alertBox = document.getElementById('alertBox');
            try {
                const res = await apiCall('/auth/login', 'POST', {
                    email: document.getElementById('email').value,
                    password: document.getElementById('password').value
                });
                localStorage.setItem('token', res.token);
                localStorage.setItem('user', JSON.stringify(res.user));
                
                if(res.user.role === 'admin') window.location.href = '/admin/dashboard.html';
                else if(res.user.role === 'staff') window.location.href = '/staff/dashboard.html';
                else window.location.href = '/dashboard.html';
            } catch (err) {
                alertBox.textContent = err.message;
                alertBox.className = 'alert alert-error';
                alertBox.style.display = 'block';
            }
        });
    </script>
</body>
</html>
""",
    "frontend/signup.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Sign Up - Complaint Routing System</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <div class="auth-container card">
        <h2 style="text-align: center; margin-bottom: 1.5rem; color: var(--primary)">Create Account</h2>
        <div id="alertBox" class="alert"></div>
        <form id="signupForm">
            <div class="form-group">
                <label>Full Name</label>
                <input type="text" id="name" required>
            </div>
            <div class="form-group">
                <label>Email</label>
                <input type="email" id="email" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" id="password" required>
            </div>
            <div class="form-group">
                <label>Confirm Password</label>
                <input type="password" id="cpassword" required>
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%">Sign Up</button>
        </form>
        <p style="text-align: center; margin-top: 1rem">
            Already have an account? <a href="/index.html">Login</a>
        </p>
    </div>

    <script src="/js/api.js"></script>
    <script>
        document.getElementById('signupForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const alertBox = document.getElementById('alertBox');
            const pass = document.getElementById('password').value;
            const cpass = document.getElementById('cpassword').value;
            
            if (pass !== cpass) {
                alertBox.textContent = "Passwords do not match";
                alertBox.className = 'alert alert-error';
                alertBox.style.display = 'block';
                return;
            }

            try {
                await apiCall('/auth/signup', 'POST', {
                    name: document.getElementById('name').value,
                    email: document.getElementById('email').value,
                    password: pass
                });
                alertBox.textContent = "Account created. You can now login.";
                alertBox.className = 'alert alert-success';
                alertBox.style.display = 'block';
                setTimeout(() => window.location.href = '/index.html', 2000);
            } catch (err) {
                alertBox.textContent = err.message;
                alertBox.className = 'alert alert-error';
                alertBox.style.display = 'block';
            }
        });
    </script>
</body>
</html>
""",
    "frontend/dashboard.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dashboard</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="navbar-brand">Complaint System</div>
        <div class="navbar-menu" id="navbar-menu"></div>
    </nav>
    <div class="container">
        <h2>User Dashboard</h2>
        <div class="grid-cards" style="margin-top: 1rem;">
            <div class="stat-card"><h3>Total Complaints</h3><div class="value" id="t-total">0</div></div>
            <div class="stat-card"><h3>Pending</h3><div class="value" id="t-pending">0</div></div>
            <div class="stat-card"><h3>In Progress</h3><div class="value" id="t-inprogress">0</div></div>
            <div class="stat-card"><h3>Resolved</h3><div class="value" id="t-resolved">0</div></div>
        </div>
        
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3>Recent Complaints</h3>
                <a href="/submit-complaint.html" class="btn btn-primary">New Complaint</a>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Title</th>
                        <th>Department</th>
                        <th>Status</th>
                        <th>Date</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody id="complaintsTable"></tbody>
            </table>
        </div>
    </div>
    
    <script src="/js/api.js"></script>
    <script src="/js/auth.js"></script>
    <script>
        const user = checkAuth(['user']);
        setupNavbar(user);
        
        async function load() {
            const complaints = await apiCall('/complaints');
            
            document.getElementById('t-total').innerText = complaints.length;
            document.getElementById('t-pending').innerText = complaints.filter(c => c.status === 'Pending' || c.status === 'Routed' || c.status === 'Assigned').length;
            document.getElementById('t-inprogress').innerText = complaints.filter(c => c.status === 'In Progress').length;
            document.getElementById('t-resolved').innerText = complaints.filter(c => c.status === 'Resolved').length;
            
            const tbody = document.getElementById('complaintsTable');
            tbody.innerHTML = complaints.slice(0, 5).map(c => `
                <tr>
                    <td>#${c.id}</td>
                    <td>${c.title}</td>
                    <td>${c.department_name || 'Unassigned'}</td>
                    <td><span class="badge badge-${c.status.replace(' ','')}">${c.status}</span></td>
                    <td>${new Date(c.created_at).toLocaleDateString()}</td>
                    <td><a href="/complaint-details.html?id=${c.id}" class="btn btn-primary" style="padding: 0.25rem 0.5rem; font-size: 0.875rem;">View</a></td>
                </tr>
            `).join('');
        }
        load();
    </script>
</body>
</html>
""",
    "frontend/submit-complaint.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Submit Complaint</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="navbar-brand">Complaint System</div>
        <div class="navbar-menu" id="navbar-menu"></div>
    </nav>
    <div class="container">
        <div class="card" style="max-width: 600px; margin: 0 auto;">
            <h2>Submit New Complaint</h2>
            <div id="alertBox" class="alert"></div>
            <form id="complaintForm" style="margin-top: 1rem;">
                <div class="form-group">
                    <label>Title</label>
                    <input type="text" id="title" required placeholder="Brief title of the issue">
                </div>
                <div class="form-group">
                    <label>Category</label>
                    <select id="category" required>
                        <option value="IT / Network">IT / Network</option>
                        <option value="Electrical">Electrical</option>
                        <option value="Plumbing">Plumbing</option>
                        <option value="Maintenance">Maintenance</option>
                        <option value="Housekeeping">Housekeeping</option>
                        <option value="Security">Security</option>
                        <option value="Transport">Transport</option>
                        <option value="Academic Support">Academic Support</option>
                        <option value="Administration">Administration</option>
                        <option value="Other">Other</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Location</label>
                    <input type="text" id="location" required placeholder="e.g. Room 101, Block A">
                </div>
                <div class="form-group">
                    <label>Priority (Optional)</label>
                    <select id="priority">
                        <option value="Low">Low</option>
                        <option value="Medium">Medium</option>
                        <option value="High">High</option>
                        <option value="Urgent">Urgent</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Description</label>
                    <textarea id="description" rows="5" required placeholder="Detailed description of the problem..."></textarea>
                </div>
                <button type="submit" class="btn btn-primary" style="width: 100%">Submit Complaint</button>
            </form>
        </div>
    </div>
    
    <script src="/js/api.js"></script>
    <script src="/js/auth.js"></script>
    <script>
        const user = checkAuth(['user']);
        setupNavbar(user);
        
        document.getElementById('complaintForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const alertBox = document.getElementById('alertBox');
            try {
                const res = await apiCall('/complaints', 'POST', {
                    title: document.getElementById('title').value,
                    category: document.getElementById('category').value,
                    location: document.getElementById('location').value,
                    priority: document.getElementById('priority').value,
                    description: document.getElementById('description').value
                });
                alertBox.textContent = res.message;
                alertBox.className = 'alert alert-success';
                alertBox.style.display = 'block';
                setTimeout(() => window.location.href = `/complaint-details.html?id=${res.complaintId}`, 2000);
            } catch (err) {
                alertBox.textContent = err.message;
                alertBox.className = 'alert alert-error';
                alertBox.style.display = 'block';
            }
        });
    </script>
</body>
</html>
""",
    "frontend/complaint-details.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Complaint Details</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="navbar-brand">Complaint System</div>
        <div class="navbar-menu" id="navbar-menu"></div>
    </nav>
    <div class="container">
        <div class="card" id="detailsCard">Loading...</div>
        
        <div class="card" id="timelineCard" style="display:none;">
            <h3>Status Timeline</h3>
            <div class="timeline" id="timeline"></div>
        </div>

        <div class="card" id="updateFormCard" style="display:none;">
            <h3>Update Status</h3>
            <div id="alertBox" class="alert"></div>
            <form id="updateForm">
                <div class="form-group">
                    <label>New Status</label>
                    <select id="newStatus">
                        <option value="Assigned">Assigned</option>
                        <option value="In Progress">In Progress</option>
                        <option value="Resolved">Resolved</option>
                        <option value="Rejected">Rejected</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Comment</label>
                    <textarea id="comment" rows="3" required></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Update Complaint</button>
            </form>
        </div>
        
        <div class="card" id="historyCard" style="display:none;">
            <h3>Update History</h3>
            <table style="margin-top: 1rem;">
                <thead><tr><th>Date</th><th>Updated By</th><th>Status Change</th><th>Comment</th></tr></thead>
                <tbody id="historyTable"></tbody>
            </table>
        </div>
    </div>
    
    <script src="/js/api.js"></script>
    <script src="/js/auth.js"></script>
    <script>
        const user = checkAuth();
        setupNavbar(user);
        
        const params = new URLSearchParams(window.location.search);
        const cid = params.get('id');
        
        const stages = ['Submitted', 'Routed', 'Assigned', 'In Progress', 'Resolved'];
        
        async function load() {
            try {
                const c = await apiCall(`/complaints/${cid}`);
                
                document.getElementById('detailsCard').innerHTML = `
                    <div style="display: flex; justify-content: space-between;">
                        <h2>#${c.id} - ${c.title}</h2>
                        <div>
                            <span class="badge badge-${c.status.replace(' ','')}">${c.status}</span>
                            <span class="badge badge-${c.priority}">${c.priority}</span>
                        </div>
                    </div>
                    <p style="margin-top:1rem;"><strong>Requester:</strong> ${c.creator_name || 'N/A'}</p>
                    <p><strong>Department:</strong> ${c.department_name || 'Pending routing'}</p>
                    <p><strong>Assigned Staff:</strong> ${c.assigned_staff_name || 'Unassigned'}</p>
                    <p><strong>Location:</strong> ${c.location}</p>
                    <p><strong>Category:</strong> ${c.category}</p>
                    <p><strong>Submitted:</strong> ${new Date(c.created_at).toLocaleString()}</p>
                    <hr style="margin: 1rem 0; border: none; border-top: 1px solid var(--border);">
                    <p><strong>Description:</strong><br>${c.description}</p>
                `;
                
                // Timeline
                document.getElementById('timelineCard').style.display = 'block';
                let currentStageIdx = 0;
                if(c.status === 'Routed') currentStageIdx = 1;
                if(c.status === 'Assigned') currentStageIdx = 2;
                if(c.status === 'In Progress') currentStageIdx = 3;
                if(c.status === 'Resolved') currentStageIdx = 4;
                if(c.status === 'Rejected') currentStageIdx = -1; // hide standard timeline
                
                if (c.status !== 'Rejected') {
                    document.getElementById('timeline').innerHTML = stages.map((s, i) => {
                        let cls = 'timeline-step';
                        if (i < currentStageIdx) cls += ' completed';
                        else if (i === currentStageIdx) cls += ' active';
                        return `<div class="${cls}">${s}</div>`;
                    }).join('');
                } else {
                    document.getElementById('timeline').innerHTML = `<div class="timeline-step completed" style="background:var(--danger); border-color:var(--danger)">Rejected</div>`;
                }

                // Show update form for staff/admin
                if (user.role === 'staff' || user.role === 'admin') {
                    if (c.status !== 'Resolved' && c.status !== 'Rejected') {
                        document.getElementById('updateFormCard').style.display = 'block';
                        document.getElementById('newStatus').value = c.status;
                    }
                }
                
                // History
                if (c.updates && c.updates.length > 0) {
                    document.getElementById('historyCard').style.display = 'block';
                    document.getElementById('historyTable').innerHTML = c.updates.map(u => `
                        <tr>
                            <td>${new Date(u.created_at).toLocaleString()}</td>
                            <td>${u.updater_name}</td>
                            <td>${u.old_status} &rarr; ${u.new_status}</td>
                            <td>${u.comment}</td>
                        </tr>
                    `).join('');
                }
            } catch(e) {
                document.getElementById('detailsCard').innerHTML = `<p class="alert alert-error" style="display:block">Error loading complaint: ${e.message}</p>`;
            }
        }
        
        document.getElementById('updateForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const alertBox = document.getElementById('alertBox');
            try {
                await apiCall(`/complaints/${cid}/update`, 'POST', {
                    status: document.getElementById('newStatus').value,
                    comment: document.getElementById('comment').value
                });
                alertBox.textContent = 'Updated successfully';
                alertBox.className = 'alert alert-success';
                alertBox.style.display = 'block';
                setTimeout(() => window.location.reload(), 1000);
            } catch (err) {
                alertBox.textContent = err.message;
                alertBox.className = 'alert alert-error';
                alertBox.style.display = 'block';
            }
        });
        
        load();
    </script>
</body>
</html>
""",
    "frontend/notifications.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Notifications</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="navbar-brand">Complaint System</div>
        <div class="navbar-menu" id="navbar-menu"></div>
    </nav>
    <div class="container">
        <div class="card">
            <div style="display:flex; justify-content: space-between; align-items:center;">
                <h2>Notifications</h2>
                <button class="btn btn-primary" onclick="markAllRead()">Mark all as read</button>
            </div>
            <div id="notifList" style="margin-top: 1rem;">Loading...</div>
        </div>
    </div>
    
    <script src="/js/api.js"></script>
    <script src="/js/auth.js"></script>
    <script>
        const user = checkAuth();
        setupNavbar(user);
        
        async function load() {
            const list = await apiCall('/notifications');
            const div = document.getElementById('notifList');
            if (list.length === 0) {
                div.innerHTML = '<p>No notifications.</p>';
                return;
            }
            div.innerHTML = list.map(n => `
                <div style="padding: 1rem; border: 1px solid var(--border); margin-bottom: 0.5rem; border-radius: 0.25rem; background: ${n.is_read ? 'transparent' : '#f0f9ff'};">
                    <p style="margin-bottom: 0.5rem">${n.message}</p>
                    <small style="color:var(--text-muted)">${new Date(n.created_at).toLocaleString()}</small>
                    ${n.complaint_id ? `<a href="/complaint-details.html?id=${n.complaint_id}" class="btn" style="padding: 0.25rem; background:var(--border); font-size:0.75rem; margin-left:1rem;">View Complaint</a>` : ''}
                    ${!n.is_read ? `<button onclick="markRead(${n.id})" class="btn" style="padding: 0.25rem; background:var(--success); color:white; font-size:0.75rem; margin-left:0.5rem;">Mark Read</button>` : ''}
                </div>
            `).join('');
        }
        
        async function markRead(id) {
            await apiCall(`/notifications/${id}/read`, 'PUT');
            load();
            fetchUnreadNotifications();
        }
        async function markAllRead() {
            await apiCall(`/notifications/read-all`, 'PUT');
            load();
            fetchUnreadNotifications();
        }
        
        load();
    </script>
</body>
</html>
""",
    "frontend/complaints.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Complaints</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="navbar-brand">Complaint System</div>
        <div class="navbar-menu" id="navbar-menu"></div>
    </nav>
    <div class="container">
        <div class="card">
            <h2>My Complaints</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Title</th>
                        <th>Department</th>
                        <th>Status</th>
                        <th>Priority</th>
                        <th>Date</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody id="complaintsTable"></tbody>
            </table>
        </div>
    </div>
    
    <script src="/js/api.js"></script>
    <script src="/js/auth.js"></script>
    <script>
        const user = checkAuth(['user']);
        setupNavbar(user);
        
        async function load() {
            const complaints = await apiCall('/complaints');
            const tbody = document.getElementById('complaintsTable');
            if (complaints.length === 0) tbody.innerHTML = '<tr><td colspan="7">No complaints found.</td></tr>';
            else tbody.innerHTML = complaints.map(c => `
                <tr>
                    <td>#${c.id}</td>
                    <td>${c.title}</td>
                    <td>${c.department_name || 'Unassigned'}</td>
                    <td><span class="badge badge-${c.status.replace(' ','')}">${c.status}</span></td>
                    <td><span class="badge badge-${c.priority}">${c.priority}</span></td>
                    <td>${new Date(c.created_at).toLocaleDateString()}</td>
                    <td><a href="/complaint-details.html?id=${c.id}" class="btn btn-primary" style="padding: 0.25rem 0.5rem; font-size: 0.875rem;">View</a></td>
                </tr>
            `).join('');
        }
        load();
    </script>
</body>
</html>
""",
    "frontend/admin/dashboard.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Admin Dashboard</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="navbar-brand">Admin Panel</div>
        <div class="navbar-menu" id="navbar-menu"></div>
    </nav>
    <div class="container">
        <h2>System Overview</h2>
        <div class="grid-cards" style="margin-top: 1rem;">
            <div class="stat-card"><h3>Total Users</h3><div class="value" id="s-users">0</div></div>
            <div class="stat-card"><h3>Total Complaints</h3><div class="value" id="s-complaints">0</div></div>
            <div class="stat-card"><h3>Pending</h3><div class="value" id="s-pending">0</div></div>
            <div class="stat-card"><h3>In Progress</h3><div class="value" id="s-inprogress">0</div></div>
            <div class="stat-card"><h3>Resolved</h3><div class="value" id="s-resolved">0</div></div>
            <div class="stat-card"><h3>Urgent</h3><div class="value" id="s-urgent" style="color:var(--danger)">0</div></div>
        </div>
        
        <div class="card">
            <h3>Recent Complaints</h3>
            <table>
                <thead><tr><th>ID</th><th>Title</th><th>Dept</th><th>Status</th><th>Priority</th><th>Action</th></tr></thead>
                <tbody id="c-table"></tbody>
            </table>
        </div>
    </div>
    
    <script src="/js/api.js"></script>
    <script src="/js/auth.js"></script>
    <script>
        const user = checkAuth(['admin']);
        setupNavbar(user);
        
        async function load() {
            const stats = await apiCall('/admin/stats');
            document.getElementById('s-users').innerText = stats.users;
            document.getElementById('s-complaints').innerText = stats.complaints;
            document.getElementById('s-pending').innerText = stats.pending;
            document.getElementById('s-inprogress').innerText = stats.inProgress;
            document.getElementById('s-resolved').innerText = stats.resolved;
            document.getElementById('s-urgent').innerText = stats.urgent;
            
            const complaints = await apiCall('/complaints');
            const tbody = document.getElementById('c-table');
            tbody.innerHTML = complaints.slice(0,10).map(c => `
                <tr>
                    <td>#${c.id}</td>
                    <td>${c.title}</td>
                    <td>${c.department_name || '-'}</td>
                    <td><span class="badge badge-${c.status.replace(' ','')}">${c.status}</span></td>
                    <td><span class="badge badge-${c.priority}">${c.priority}</span></td>
                    <td><a href="/complaint-details.html?id=${c.id}" class="btn btn-primary" style="padding: 0.25rem">View</a></td>
                </tr>
            `).join('');
        }
        load();
    </script>
</body>
</html>
""",
    "frontend/admin/complaints.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Manage Complaints</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="navbar-brand">Admin Panel</div>
        <div class="navbar-menu" id="navbar-menu"></div>
    </nav>
    <div class="container">
        <div class="card">
            <h2>All Complaints</h2>
            <div style="margin: 1rem 0; display:flex; gap:1rem;">
                <input type="text" id="search" placeholder="Search title..." oninput="render()" style="width: 250px;">
                <select id="f-status" onchange="render()"><option value="">All Statuses</option><option value="Pending">Pending</option><option value="In Progress">In Progress</option><option value="Resolved">Resolved</option></select>
            </div>
            <table>
                <thead><tr><th>ID</th><th>Title</th><th>Dept</th><th>Status</th><th>Priority</th><th>Date</th><th>Action</th></tr></thead>
                <tbody id="c-table"></tbody>
            </table>
        </div>
    </div>
    
    <script src="/js/api.js"></script>
    <script src="/js/auth.js"></script>
    <script>
        const user = checkAuth(['admin']);
        setupNavbar(user);
        let allC = [];
        
        async function load() {
            allC = await apiCall('/complaints');
            render();
        }
        function render() {
            const q = document.getElementById('search').value.toLowerCase();
            const s = document.getElementById('f-status').value;
            let f = allC.filter(c => c.title.toLowerCase().includes(q));
            if(s) f = f.filter(c => c.status === s);
            
            document.getElementById('c-table').innerHTML = f.map(c => `
                <tr>
                    <td>#${c.id}</td>
                    <td>${c.title}</td>
                    <td>${c.department_name || '-'}</td>
                    <td><span class="badge badge-${c.status.replace(' ','')}">${c.status}</span></td>
                    <td><span class="badge badge-${c.priority}">${c.priority}</span></td>
                    <td>${new Date(c.created_at).toLocaleDateString()}</td>
                    <td><a href="/complaint-details.html?id=${c.id}" class="btn btn-primary" style="padding: 0.25rem">View</a></td>
                </tr>
            `).join('');
        }
        load();
    </script>
</body>
</html>
""",
    "frontend/admin/departments.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Departments</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="navbar-brand">Admin Panel</div>
        <div class="navbar-menu" id="navbar-menu"></div>
    </nav>
    <div class="container">
        <div class="card">
            <h3>Add Department</h3>
            <form id="addForm" style="display:flex; gap:1rem; align-items:end;">
                <div class="form-group" style="flex:1; margin:0;"><label>Name</label><input type="text" id="n" required></div>
                <div class="form-group" style="flex:2; margin:0;"><label>Description</label><input type="text" id="d" required></div>
                <button type="submit" class="btn btn-primary">Add</button>
            </form>
        </div>
        <div class="card">
            <h2>Departments</h2>
            <table>
                <thead><tr><th>ID</th><th>Name</th><th>Description</th><th>Staff Count</th><th>Complaints</th><th>Action</th></tr></thead>
                <tbody id="d-table"></tbody>
            </table>
        </div>
    </div>
    
    <script src="/js/api.js"></script>
    <script src="/js/auth.js"></script>
    <script>
        const user = checkAuth(['admin']);
        setupNavbar(user);
        
        async function load() {
            const list = await apiCall('/departments');
            document.getElementById('d-table').innerHTML = list.map(d => `
                <tr>
                    <td>${d.id}</td>
                    <td>${d.name}</td>
                    <td>${d.description}</td>
                    <td>${d.staff_count}</td>
                    <td>${d.complaint_count}</td>
                    <td><button onclick="del(${d.id})" class="btn" style="padding:0.25rem; background:var(--danger); color:white;">Delete</button></td>
                </tr>
            `).join('');
        }
        
        document.getElementById('addForm').addEventListener('submit', async(e)=>{
            e.preventDefault();
            await apiCall('/departments', 'POST', {name: document.getElementById('n').value, description: document.getElementById('d').value});
            document.getElementById('addForm').reset();
            load();
        });
        
        async function del(id) {
            if(!confirm('Are you sure?')) return;
            try {
                await apiCall(`/departments/${id}`, 'DELETE');
                load();
            } catch(e) { alert(e.message); }
        }
        load();
    </script>
</body>
</html>
""",
    "frontend/admin/users.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Users</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="navbar-brand">Admin Panel</div>
        <div class="navbar-menu" id="navbar-menu"></div>
    </nav>
    <div class="container">
        <div class="card">
            <h2>Users & Staff</h2>
            <table>
                <thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Role</th><th>Department</th><th>Action</th></tr></thead>
                <tbody id="u-table"></tbody>
            </table>
        </div>
    </div>
    
    <script src="/js/api.js"></script>
    <script src="/js/auth.js"></script>
    <script>
        const user = checkAuth(['admin']);
        setupNavbar(user);
        
        let depts = [];
        
        async function load() {
            depts = await apiCall('/departments');
            const list = await apiCall('/users');
            
            document.getElementById('u-table').innerHTML = list.map(u => `
                <tr>
                    <td>${u.id}</td>
                    <td>${u.name}</td>
                    <td>${u.email}</td>
                    <td><span class="badge" style="background:#e2e8f0; color:#0f172a">${u.role.toUpperCase()}</span></td>
                    <td>${u.department_name || '-'}</td>
                    <td>
                        ${u.role !== 'admin' ? `
                            <select onchange="assignDept(${u.id}, this.value)" style="width:auto; padding:0.25rem;">
                                <option value="">Assign Dept...</option>
                                ${depts.map(d => `<option value="${d.id}" ${u.department_name===d.name?'selected':''}>${d.name}</option>`).join('')}
                            </select>
                        ` : ''}
                    </td>
                </tr>
            `).join('');
        }
        
        async function assignDept(uid, did) {
            if(!did) return;
            try {
                await apiCall(`/users/${uid}/department`, 'PUT', {department_id: did});
                alert('Assigned successfully (user is now staff)');
                load();
            } catch(e) { alert(e.message); }
        }
        load();
    </script>
</body>
</html>
""",
    "frontend/staff/dashboard.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Staff Dashboard</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="navbar-brand">Staff Panel</div>
        <div class="navbar-menu" id="navbar-menu"></div>
    </nav>
    <div class="container">
        <h2>Staff Dashboard</h2>
        <div class="grid-cards" style="margin-top: 1rem;">
            <div class="stat-card"><h3>Assigned</h3><div class="value" id="s-assigned">0</div></div>
            <div class="stat-card"><h3>Pending</h3><div class="value" id="s-pending">0</div></div>
            <div class="stat-card"><h3>In Progress</h3><div class="value" id="s-inprogress">0</div></div>
            <div class="stat-card"><h3>Resolved</h3><div class="value" id="s-resolved">0</div></div>
            <div class="stat-card"><h3>Urgent</h3><div class="value" id="s-urgent" style="color:var(--danger)">0</div></div>
        </div>
        
        <div class="card">
            <h3>My Tasks</h3>
            <table>
                <thead><tr><th>ID</th><th>Title</th><th>Status</th><th>Priority</th><th>Action</th></tr></thead>
                <tbody id="c-table"></tbody>
            </table>
        </div>
    </div>
    
    <script src="/js/api.js"></script>
    <script src="/js/auth.js"></script>
    <script>
        const user = checkAuth(['staff']);
        setupNavbar(user);
        
        async function load() {
            const stats = await apiCall('/staff/stats');
            document.getElementById('s-assigned').innerText = stats.assigned;
            document.getElementById('s-pending').innerText = stats.pending;
            document.getElementById('s-inprogress').innerText = stats.inProgress;
            document.getElementById('s-resolved').innerText = stats.resolved;
            document.getElementById('s-urgent').innerText = stats.urgent;
            
            const complaints = await apiCall('/complaints');
            const tbody = document.getElementById('c-table');
            // Filter only assigned to this staff or belonging to their dept but unassigned
            tbody.innerHTML = complaints.filter(c => c.assigned_staff_id === user.id || !c.assigned_staff_id).slice(0,10).map(c => `
                <tr>
                    <td>#${c.id}</td>
                    <td>${c.title}</td>
                    <td><span class="badge badge-${c.status.replace(' ','')}">${c.status}</span></td>
                    <td><span class="badge badge-${c.priority}">${c.priority}</span></td>
                    <td><a href="/complaint-details.html?id=${c.id}" class="btn btn-primary" style="padding: 0.25rem">View / Update</a></td>
                </tr>
            `).join('');
        }
        load();
    </script>
</body>
</html>
""",
    "frontend/staff/complaints.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Staff Complaints</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="navbar-brand">Staff Panel</div>
        <div class="navbar-menu" id="navbar-menu"></div>
    </nav>
    <div class="container">
        <div class="card">
            <h2>Department Complaints</h2>
            <table>
                <thead><tr><th>ID</th><th>Title</th><th>Status</th><th>Priority</th><th>Date</th><th>Action</th></tr></thead>
                <tbody id="c-table"></tbody>
            </table>
        </div>
    </div>
    
    <script src="/js/api.js"></script>
    <script src="/js/auth.js"></script>
    <script>
        const user = checkAuth(['staff']);
        setupNavbar(user);
        
        async function load() {
            const complaints = await apiCall('/complaints');
            document.getElementById('c-table').innerHTML = complaints.map(c => `
                <tr>
                    <td>#${c.id}</td>
                    <td>${c.title}</td>
                    <td><span class="badge badge-${c.status.replace(' ','')}">${c.status}</span></td>
                    <td><span class="badge badge-${c.priority}">${c.priority}</span></td>
                    <td>${new Date(c.created_at).toLocaleDateString()}</td>
                    <td><a href="/complaint-details.html?id=${c.id}" class="btn btn-primary" style="padding: 0.25rem">View / Update</a></td>
                </tr>
            `).join('');
        }
        load();
    </script>
</body>
</html>
"""
}

for path, content in frontend_files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Generated frontend files")
