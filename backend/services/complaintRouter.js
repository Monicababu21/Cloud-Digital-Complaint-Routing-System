const db = require('../config/db');

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
