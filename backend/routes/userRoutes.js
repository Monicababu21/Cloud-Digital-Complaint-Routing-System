const express = require('express');
const router = express.Router();
const controller = require('../controllers/userController');
const auth = require('../middleware/authMiddleware');
const role = require('../middleware/roleMiddleware');

router.use(auth);
router.get('/', role(['admin']), controller.getAll);
router.put('/:id/department', role(['admin']), controller.updateDepartment);

module.exports = router;
