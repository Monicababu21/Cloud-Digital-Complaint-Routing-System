import os

base_dir = "c:/Users/monica/OneDrive/Documents/CLOUD/Cloud-Digital-Complaint-Routing-System"

files = {
    "database/schema.sql": """CREATE DATABASE IF NOT EXISTS complaint_routing;
USE complaint_routing;

CREATE TABLE departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('user', 'staff', 'admin') DEFAULT 'user',
    department_id INT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
);

CREATE TABLE complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    department_id INT DEFAULT NULL,
    assigned_staff_id INT DEFAULT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(255) NOT NULL,
    priority ENUM('Low', 'Medium', 'High', 'Urgent') DEFAULT 'Low',
    status ENUM('Pending', 'Routed', 'Assigned', 'In Progress', 'Resolved', 'Rejected') DEFAULT 'Pending',
    location VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL,
    FOREIGN KEY (assigned_staff_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    complaint_id INT DEFAULT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (complaint_id) REFERENCES complaints(id) ON DELETE CASCADE
);

CREATE TABLE complaint_updates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    complaint_id INT NOT NULL,
    updated_by INT NOT NULL,
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (complaint_id) REFERENCES complaints(id) ON DELETE CASCADE,
    FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE CASCADE
);

-- Seed Data
INSERT INTO departments (name, description) VALUES 
('IT Support', 'Handles networking, computers, projectors, etc.'),
('Maintenance', 'Handles furniture, doors, windows, etc.'),
('Electrical', 'Handles lights, fans, power, etc.'),
('Plumbing', 'Handles water, drainage, toilets, etc.'),
('Housekeeping', 'Handles cleaning, dust, waste.'),
('Security', 'Handles theft, suspicious activity, access.'),
('Transport', 'Handles buses, routes, drivers.'),
('Academic Support', 'Handles timetable, faculty issues.'),
('Administration', 'Handles documents, fees.');

-- Passwords are all 'password123' bcrypt hashed (cost 10)
INSERT INTO users (name, email, password, role, department_id) VALUES 
('Admin User', 'admin@complaints.com', '$2b$10$EP0/7Wq.iZ1bC9/F.u2rRe9QzD9r/LqD9bOqH3H.Z2X2uJ0sJ/z.', 'admin', NULL),
('IT Staff', 'itstaff@complaints.com', '$2b$10$EP0/7Wq.iZ1bC9/F.u2rRe9QzD9r/LqD9bOqH3H.Z2X2uJ0sJ/z.', 'staff', 1),
('Student User', 'student@complaints.com', '$2b$10$EP0/7Wq.iZ1bC9/F.u2rRe9QzD9r/LqD9bOqH3H.Z2X2uJ0sJ/z.', 'user', NULL);
""",
    "backend/middleware/authMiddleware.js": """const jwt = require('jsonwebtoken');

module.exports = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];
    
    if (!token) return res.status(401).json({ message: 'No token provided' });
    
    jwt.verify(token, process.env.JWT_SECRET, (err, decoded) => {
        if (err) return res.status(403).json({ message: 'Invalid token' });
        req.user = decoded;
        next();
    });
};
""",
    "backend/middleware/roleMiddleware.js": """module.exports = (roles) => {
    return (req, res, next) => {
        if (!req.user || !roles.includes(req.user.role)) {
            return res.status(403).json({ message: 'Access denied' });
        }
        next();
    };
};
""",
    "backend/controllers/authController.js": """const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const db = require('../config/db');

exports.signup = async (req, res) => {
    try {
        const { name, email, password } = req.body;
        if (!name || !email || !password) return res.status(400).json({ message: 'All fields are required' });
        
        const [existing] = await db.query('SELECT * FROM users WHERE email = ?', [email]);
        if (existing.length > 0) return res.status(400).json({ message: 'Email already exists' });
        
        const hashedPassword = await bcrypt.hash(password, 10);
        const [result] = await db.query('INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)', [name, email, hashedPassword, 'user']);
        
        res.status(201).json({ message: 'User registered successfully', userId: result.insertId });
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
};

exports.login = async (req, res) => {
    try {
        const { email, password } = req.body;
        const [users] = await db.query('SELECT * FROM users WHERE email = ?', [email]);
        if (users.length === 0) return res.status(401).json({ message: 'Invalid email or password' });
        
        const user = users[0];
        const match = await bcrypt.compare(password, user.password);
        if (!match) return res.status(401).json({ message: 'Invalid email or password' });
        
        const token = jwt.sign({ id: user.id, role: user.role, name: user.name }, process.env.JWT_SECRET, { expiresIn: process.env.JWT_EXPIRES_IN || '7d' });
        res.json({ token, user: { id: user.id, name: user.name, role: user.role } });
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
};

exports.me = async (req, res) => {
    try {
        const [users] = await db.query('SELECT id, name, email, role, department_id, created_at FROM users WHERE id = ?', [req.user.id]);
        if (users.length === 0) return res.status(404).json({ message: 'User not found' });
        res.json(users[0]);
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
};
""",
    "backend/routes/authRoutes.js": """const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');
const authMiddleware = require('../middleware/authMiddleware');

router.post('/signup', authController.signup);
router.post('/login', authController.login);
router.get('/me', authMiddleware, authController.me);

module.exports = router;
""",
    "backend/services/complaintRouter.js": """const db = require('../config/db');

const keywords = {
    'IT Support': ['wifi', 'internet', 'network', 'computer', 'laptop', 'projector', 'printer', 'software', 'login', 'server'],
    'Electrical': ['light', 'electricity', 'fan', 'switch', 'socket', 'power', 'wiring', 'voltage'],
    'Plumbing': ['water', 'tap', 'pipe', 'leakage', 'toilet', 'washroom', 'drainage'],
    'Maintenance': ['furniture', 'chair', 'table', 'door', 'window', 'wall', 'ceiling', 'broken'],
    'Housekeeping': ['cleaning', 'garbage', 'dust', 'dirty', 'waste', 'restroom cleaning'],
    'Security': ['theft', 'lost', 'suspicious', 'security', 'access', 'gate'],
    'Transport': ['bus', 'vehicle', 'transport', 'driver', 'route'],
    'Academic Support': ['classroom', 'faculty', 'timetable', 'exam', 'assignment', 'course'],
    'Administration': ['document', 'certificate', 'office', 'fee', 'registration']
};

exports.routeComplaint = async (title, description, category) => {
    const text = `${title} ${description} ${category}`.toLowerCase();
    
    let matchedDeptName = category; // fallback
    let maxMatches = 0;

    for (const [dept, words] of Object.entries(keywords)) {
        let matches = words.filter(word => text.includes(word)).length;
        if (matches > maxMatches) {
            maxMatches = matches;
            matchedDeptName = dept;
        }
    }

    try {
        let [depts] = await db.query('SELECT id FROM departments WHERE name LIKE ?', [`%${matchedDeptName}%`]);
        let deptId = depts.length > 0 ? depts[0].id : null;
        
        let assignedStaffId = null;
        if (deptId) {
            const [staff] = await db.query(`
                SELECT u.id, (SELECT COUNT(*) FROM complaints c WHERE c.assigned_staff_id = u.id AND c.status NOT IN ('Resolved', 'Rejected')) as active_count
                FROM users u WHERE u.department_id = ? AND u.role = 'staff'
                ORDER BY active_count ASC LIMIT 1
            `, [deptId]);
            if (staff.length > 0) assignedStaffId = staff[0].id;
        }
        
        return { deptId, assignedStaffId, matchedDeptName };
    } catch(e) {
        console.error('Routing error:', e);
        return { deptId: null, assignedStaffId: null, matchedDeptName: 'Unknown' };
    }
};

exports.detectPriority = (text) => {
    const urgentWords = ['emergency', 'dangerous', 'fire', 'threat', 'power failure'];
    const highWords = ['urgent', 'fast', 'quick', 'immediate'];
    const lower = text.toLowerCase();
    if (urgentWords.some(w => lower.includes(w))) return 'Urgent';
    if (highWords.some(w => lower.includes(w))) return 'High';
    return null;
};
""",
    "backend/controllers/complaintController.js": """const db = require('../config/db');
const routerService = require('../services/complaintRouter');

exports.createComplaint = async (req, res) => {
    try {
        const { title, description, category, location, priority } = req.body;
        const userId = req.user.id;
        
        const autoPriority = routerService.detectPriority(`${title} ${description}`);
        const finalPriority = (autoPriority === 'Urgent' || priority === 'Urgent') ? 'Urgent' : (autoPriority || priority || 'Low');
        
        const { deptId, assignedStaffId, matchedDeptName } = await routerService.routeComplaint(title, description, category);
        const status = assignedStaffId ? 'Assigned' : 'Routed';
        
        const [result] = await db.query(
            'INSERT INTO complaints (user_id, department_id, assigned_staff_id, title, description, category, priority, status, location) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            [userId, deptId, assignedStaffId, title, description, category, finalPriority, status, location]
        );
        const complaintId = result.insertId;

        // Notifications
        await db.query('INSERT INTO notifications (user_id, complaint_id, message) VALUES (?, ?, ?)', [userId, complaintId, `Your complaint has been automatically routed to ${matchedDeptName}.`]);
        if (assignedStaffId) {
            await db.query('INSERT INTO notifications (user_id, complaint_id, message) VALUES (?, ?, ?)', [assignedStaffId, complaintId, `New complaint assigned to you: ${title}`]);
        }
        
        res.status(201).json({ message: 'Complaint submitted successfully', complaintId });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error' });
    }
};

exports.getComplaints = async (req, res) => {
    try {
        let query = 'SELECT c.*, d.name as department_name, u.name as assigned_staff_name FROM complaints c LEFT JOIN departments d ON c.department_id = d.id LEFT JOIN users u ON c.assigned_staff_id = u.id';
        let params = [];
        let conditions = [];
        
        if (req.user.role === 'user') {
            conditions.push('c.user_id = ?');
            params.push(req.user.id);
        } else if (req.user.role === 'staff') {
            conditions.push('(c.assigned_staff_id = ? OR c.department_id = (SELECT department_id FROM users WHERE id = ?))');
            params.push(req.user.id, req.user.id);
        }
        
        if (req.query.status) {
            conditions.push('c.status = ?');
            params.push(req.query.status);
        }

        if (conditions.length > 0) query += ' WHERE ' + conditions.join(' AND ');
        query += ' ORDER BY c.created_at DESC';
        
        const [complaints] = await db.query(query, params);
        res.json(complaints);
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
};

exports.getComplaintById = async (req, res) => {
    try {
        const [complaint] = await db.query('SELECT c.*, d.name as department_name, u.name as assigned_staff_name, creator.name as creator_name FROM complaints c LEFT JOIN departments d ON c.department_id = d.id LEFT JOIN users u ON c.assigned_staff_id = u.id LEFT JOIN users creator ON c.user_id = creator.id WHERE c.id = ?', [req.params.id]);
        if (complaint.length === 0) return res.status(404).json({ message: 'Complaint not found' });
        
        const [updates] = await db.query('SELECT cu.*, u.name as updater_name FROM complaint_updates cu JOIN users u ON cu.updated_by = u.id WHERE cu.complaint_id = ? ORDER BY cu.created_at ASC', [req.params.id]);
        
        res.json({ ...complaint[0], updates });
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
};

exports.updateComplaintStatus = async (req, res) => {
    try {
        const { id } = req.params;
        const { status, comment } = req.body;
        
        const [complaint] = await db.query('SELECT * FROM complaints WHERE id = ?', [id]);
        if (complaint.length === 0) return res.status(404).json({ message: 'Not found' });
        
        const oldStatus = complaint[0].status;
        
        let query = 'UPDATE complaints SET status = ?, updated_at = NOW()';
        let params = [status];
        if (status === 'Resolved' || status === 'Rejected') {
            query += ', resolved_at = NOW()';
        }
        query += ' WHERE id = ?';
        params.push(id);
        
        await db.query(query, params);
        await db.query('INSERT INTO complaint_updates (complaint_id, updated_by, old_status, new_status, comment) VALUES (?, ?, ?, ?, ?)', [id, req.user.id, oldStatus, status, comment || '']);
        
        await db.query('INSERT INTO notifications (user_id, complaint_id, message) VALUES (?, ?, ?)', [complaint[0].user_id, id, `Your complaint status changed from ${oldStatus} to ${status}`]);
        
        res.json({ message: 'Updated successfully' });
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
};

exports.deleteComplaint = async (req, res) => {
    try {
        await db.query('DELETE FROM complaints WHERE id = ?', [req.params.id]);
        res.json({ message: 'Deleted' });
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
};
""",
    "backend/routes/complaintRoutes.js": """const express = require('express');
const router = express.Router();
const controller = require('../controllers/complaintController');
const auth = require('../middleware/authMiddleware');
const role = require('../middleware/roleMiddleware');

router.use(auth);

router.post('/', controller.createComplaint);
router.get('/', controller.getComplaints);
router.get('/:id', controller.getComplaintById);
router.put('/:id', role(['staff', 'admin']), controller.updateComplaintStatus);
router.post('/:id/update', role(['staff', 'admin']), controller.updateComplaintStatus);
router.delete('/:id', role(['admin']), controller.deleteComplaint);

module.exports = router;
""",
    "backend/controllers/departmentController.js": """const db = require('../config/db');

exports.getAll = async (req, res) => {
    try {
        const [departments] = await db.query('SELECT d.*, (SELECT COUNT(*) FROM users u WHERE u.department_id = d.id) as staff_count, (SELECT COUNT(*) FROM complaints c WHERE c.department_id = d.id) as complaint_count FROM departments d');
        res.json(departments);
    } catch(e) { res.status(500).json({message: 'Error'}) }
};

exports.create = async (req, res) => {
    try {
        const { name, description } = req.body;
        await db.query('INSERT INTO departments (name, description) VALUES (?, ?)', [name, description]);
        res.json({message: 'Created'});
    } catch(e) { res.status(500).json({message: 'Error'}) }
};

exports.update = async (req, res) => {
    try {
        const { name, description } = req.body;
        await db.query('UPDATE departments SET name=?, description=? WHERE id=?', [name, description, req.params.id]);
        res.json({message: 'Updated'});
    } catch(e) { res.status(500).json({message: 'Error'}) }
};

exports.delete = async (req, res) => {
    try {
        await db.query('DELETE FROM departments WHERE id=? AND (SELECT COUNT(*) FROM complaints WHERE department_id=?) = 0', [req.params.id, req.params.id]);
        res.json({message: 'Deleted (if no active complaints)'});
    } catch(e) { res.status(500).json({message: 'Error'}) }
};
""",
    "backend/routes/departmentRoutes.js": """const express = require('express');
const router = express.Router();
const controller = require('../controllers/departmentController');
const auth = require('../middleware/authMiddleware');
const role = require('../middleware/roleMiddleware');

router.use(auth);
router.get('/', controller.getAll);
router.post('/', role(['admin']), controller.create);
router.put('/:id', role(['admin']), controller.update);
router.delete('/:id', role(['admin']), controller.delete);

module.exports = router;
""",
    "backend/controllers/notificationController.js": """const db = require('../config/db');

exports.getNotifications = async (req, res) => {
    try {
        const [notifs] = await db.query('SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC', [req.user.id]);
        res.json(notifs);
    } catch(e) { res.status(500).json({message: 'Error'}) }
};

exports.readAll = async (req, res) => {
    try {
        await db.query('UPDATE notifications SET is_read = TRUE WHERE user_id = ?', [req.user.id]);
        res.json({message: 'All read'});
    } catch(e) { res.status(500).json({message: 'Error'}) }
};

exports.readOne = async (req, res) => {
    try {
        await db.query('UPDATE notifications SET is_read = TRUE WHERE id = ? AND user_id = ?', [req.params.id, req.user.id]);
        res.json({message: 'Read'});
    } catch(e) { res.status(500).json({message: 'Error'}) }
};
""",
    "backend/routes/notificationRoutes.js": """const express = require('express');
const router = express.Router();
const controller = require('../controllers/notificationController');
const auth = require('../middleware/authMiddleware');

router.use(auth);
router.get('/', controller.getNotifications);
router.put('/read-all', controller.readAll);
router.put('/:id/read', controller.readOne);

module.exports = router;
""",
    "backend/controllers/userController.js": """const db = require('../config/db');

exports.getAll = async (req, res) => {
    try {
        const [users] = await db.query('SELECT u.id, u.name, u.email, u.role, u.created_at, d.name as department_name FROM users u LEFT JOIN departments d ON u.department_id = d.id');
        res.json(users);
    } catch(e) { res.status(500).json({message: 'Error'}) }
};

exports.updateDepartment = async (req, res) => {
    try {
        await db.query('UPDATE users SET department_id = ?, role = "staff" WHERE id = ? AND role != "admin"', [req.body.department_id, req.params.id]);
        res.json({message: 'Updated'});
    } catch(e) { res.status(500).json({message: 'Error'}) }
};
""",
    "backend/routes/userRoutes.js": """const express = require('express');
const router = express.Router();
const controller = require('../controllers/userController');
const auth = require('../middleware/authMiddleware');
const role = require('../middleware/roleMiddleware');

router.use(auth);
router.get('/', role(['admin']), controller.getAll);
router.put('/:id/department', role(['admin']), controller.updateDepartment);

module.exports = router;
"""
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Generated backend files")
