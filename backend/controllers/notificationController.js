const db = require('../config/db');

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
