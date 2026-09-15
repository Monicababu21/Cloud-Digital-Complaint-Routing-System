CREATE DATABASE IF NOT EXISTS complaint_routing;
USE complaint_routing;

CREATE TABLE departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('user', 'staff', 'admin') DEFAULT 'user',
    department_id INT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
);

CREATE TABLE complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    department_id INT DEFAULT NULL,
    assigned_staff_id INT DEFAULT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(255) NOT NULL,
    priority ENUM('Low', 'Medium', 'High', 'Urgent') DEFAULT 'Low',
    status ENUM('Pending', 'Routed', 'Assigned', 'In Progress', 'Resolved', 'Rejected') DEFAULT 'Pending',
    location VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL,
    FOREIGN KEY (assigned_staff_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    complaint_id INT DEFAULT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (complaint_id) REFERENCES complaints(id) ON DELETE CASCADE
);

CREATE TABLE complaint_updates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    complaint_id INT NOT NULL,
    updated_by INT NOT NULL,
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (complaint_id) REFERENCES complaints(id) ON DELETE CASCADE,
    FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE CASCADE
);

-- Seed Data
INSERT INTO departments (name, description) VALUES 
('IT Support', 'Handles networking, computers, projectors, etc.'),
('Maintenance', 'Handles furniture, doors, windows, etc.'),
('Electrical', 'Handles lights, fans, power, etc.'),
('Plumbing', 'Handles water, drainage, toilets, etc.'),
('Housekeeping', 'Handles cleaning, dust, waste.'),
('Security', 'Handles theft, suspicious activity, access.'),
('Transport', 'Handles buses, routes, drivers.'),
('Academic Support', 'Handles timetable, faculty issues.'),
('Administration', 'Handles documents, fees.');

-- Passwords are all 'password123' bcrypt hashed (cost 10)
INSERT INTO users (name, email, password, role, department_id) VALUES 
('Admin User', 'admin@complaints.com', '$2b$10$EP0/7Wq.iZ1bC9/F.u2rRe9QzD9r/LqD9bOqH3H.Z2X2uJ0sJ/z.', 'admin', NULL),
('IT Staff', 'itstaff@complaints.com', '$2b$10$EP0/7Wq.iZ1bC9/F.u2rRe9QzD9r/LqD9bOqH3H.Z2X2uJ0sJ/z.', 'staff', 1),
('Student User', 'student@complaints.com', '$2b$10$EP0/7Wq.iZ1bC9/F.u2rRe9QzD9r/LqD9bOqH3H.Z2X2uJ0sJ/z.', 'user', NULL);
