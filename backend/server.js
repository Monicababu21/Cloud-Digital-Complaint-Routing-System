const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const path = require('path');

dotenv.config({ path: path.join(__dirname, '.env') });
// Fallback if .env is at root
if (!process.env.JWT_SECRET) {
    dotenv.config({ path: path.join(__dirname, '../.env') });
}

const app = express();

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve frontend static files
app.use(express.static(path.join(__dirname, '../frontend')));

// Routes
const authRoutes = require('./routes/authRoutes');
const complaintRoutes = require('./routes/complaintRoutes');
const departmentRoutes = require('./routes/departmentRoutes');
const notificationRoutes = require('./routes/notificationRoutes');
const userRoutes = require('./routes/userRoutes');

app.use('/api/auth', authRoutes);
app.use('/api/complaints', complaintRoutes);
app.use('/api/departments', departmentRoutes);
app.use('/api/notifications', notificationRoutes);
app.use('/api/users', userRoutes);

// Admin stats route (can be placed here or in a separate file)
app.get('/api/admin/stats', require('./middleware/authMiddleware'), require('./middleware/roleMiddleware')(['admin']), async (req, res) => {
    try {
        const db = require('./config/db');
        const [users] = await db.query('SELECT COUNT(*) as count FROM users');
        const [complaints] = await db.query('SELECT COUNT(*) as count FROM complaints');
        const [pending] = await db.query("SELECT COUNT(*) as count FROM complaints WHERE status = 'Pending'");
        const [inProgress] = await db.query("SELECT COUNT(*) as count FROM complaints WHERE status = 'In Progress'");
        const [resolved] = await db.query("SELECT COUNT(*) as count FROM complaints WHERE status = 'Resolved'");
        const [urgent] = await db.query("SELECT COUNT(*) as count FROM complaints WHERE priority = 'Urgent'");
        
        res.json({
            users: users[0].count,
            complaints: complaints[0].count,
            pending: pending[0].count,
            inProgress: inProgress[0].count,
            resolved: resolved[0].count,
            urgent: urgent[0].count
        });
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
});

// Staff stats route
app.get('/api/staff/stats', require('./middleware/authMiddleware'), require('./middleware/roleMiddleware')(['staff']), async (req, res) => {
    try {
        const db = require('./config/db');
        const staffId = req.user.id;
        const [assigned] = await db.query('SELECT COUNT(*) as count FROM complaints WHERE assigned_staff_id = ?', [staffId]);
        const [pending] = await db.query("SELECT COUNT(*) as count FROM complaints WHERE assigned_staff_id = ? AND status = 'Pending'", [staffId]);
        const [inProgress] = await db.query("SELECT COUNT(*) as count FROM complaints WHERE assigned_staff_id = ? AND status = 'In Progress'", [staffId]);
        const [resolved] = await db.query("SELECT COUNT(*) as count FROM complaints WHERE assigned_staff_id = ? AND status = 'Resolved'", [staffId]);
        const [urgent] = await db.query("SELECT COUNT(*) as count FROM complaints WHERE assigned_staff_id = ? AND priority = 'Urgent'", [staffId]);

        res.json({
            assigned: assigned[0].count,
            pending: pending[0].count,
            inProgress: inProgress[0].count,
            resolved: resolved[0].count,
            urgent: urgent[0].count
        });
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
});

// Health check
app.get('/api/health', (req, res) => {
    res.json({
        status: "OK",
        message: "Complaint Routing System API is running"
    });
});

// Fallback to index.html for frontend routing
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/index.html'));
});

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
