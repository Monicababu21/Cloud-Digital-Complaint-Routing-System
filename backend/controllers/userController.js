const db = require('../config/db');

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
