const express = require('express');
const router = express.Router();
const controller = require('../controllers/notificationController');
const auth = require('../middleware/authMiddleware');

router.use(auth);
router.get('/', controller.getNotifications);
router.put('/read-all', controller.readAll);
router.put('/:id/read', controller.readOne);

module.exports = router;
