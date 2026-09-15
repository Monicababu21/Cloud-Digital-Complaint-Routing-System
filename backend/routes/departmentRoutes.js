const express = require('express');
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
