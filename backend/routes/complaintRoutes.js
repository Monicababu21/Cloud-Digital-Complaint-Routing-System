const express = require('express');
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
