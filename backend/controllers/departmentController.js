const db = require('../config/db');

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
