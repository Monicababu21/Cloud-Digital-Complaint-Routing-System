const db = require('../config/db');
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
