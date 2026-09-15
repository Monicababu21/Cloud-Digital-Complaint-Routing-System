# Cloud-Based Digital Complaint Routing System

## Project Overview
This is a full-stack web application designed for smart, automated digital complaint routing. It allows users (e.g., students) to submit complaints which are automatically categorized and routed to the appropriate department and assigned to the available staff member with the lowest workload.

## Features
- **User Roles:** Admin, Staff, User/Student with Role-Based Access Control.
- **Smart Routing:** Rule-based engine categorizes complaints by keywords and assigns them automatically.
- **Priority Detection:** Auto-detects urgency based on keywords (e.g., "emergency", "fire").
- **Dashboards:** Separate dashboards for Admin, Staff, and Users with relevant statistics.
- **Complaint Tracking:** Visual status timeline and complete history of updates.
- **Notifications:** Real-time notifications for updates, assignments, and routing.
- **Cloud-Ready:** Uses `.env` configuration, decoupled backend/frontend, ready for deployment on platforms like Railway.

## Technology Stack
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (Fetch API).
- **Backend:** Node.js, Express.js.
- **Database:** MySQL.
- **Security:** JWT Authentication, bcrypt password hashing.

## Folder Structure
```
Cloud-Digital-Complaint-Routing-System/
├── frontend/             # HTML, CSS, JS static files
├── backend/              # Node.js Express Server
│   ├── config/           # Database configuration
│   ├── controllers/      # Route controllers
│   ├── middleware/       # JWT Auth and Role middlewares
│   ├── routes/           # API routes
│   └── services/         # Smart Routing Engine
├── database/             # schema.sql (table creation and seeds)
├── .env.example          # Example environment variables
└── server.js             # Main server entrypoint
```

## Database Setup
1. Install MySQL.
2. Log into MySQL console: `mysql -u root -p`
3. Run the SQL schema: `source database/schema.sql`

## How to run locally
1. Install dependencies:
   ```bash
   npm install
   ```
2. Set up environment variables:
   Copy `backend/.env.example` to `.env` in the root (or `backend/` directory) and update database credentials.
3. Start the server:
   ```bash
   npm start
   ```
   *The server runs on `http://localhost:5000` by default. Static frontend files are served automatically.*

## Demo Accounts (Passwords are `password123`)
- **Admin:** `admin@complaints.com`
- **Staff (IT Support):** `itstaff@complaints.com`
- **User (Student):** `student@complaints.com`

## How Complaint Routing Works
When a user submits a complaint, the `complaintRouter` service scans the `title`, `description`, and `category`. It matches text against a predefined list of keyword arrays associated with departments (e.g. IT, Maintenance, Plumbing). 
Once a department is selected, the engine finds all staff in that department and assigns the ticket to the one with the fewest currently active (unresolved) complaints. Priority is also adjusted if keywords like "urgent" or "fire" are detected.

## How to deploy to Railway
1. Push this repository to GitHub.
2. In Railway, create a new MySQL database service.
3. Connect your GitHub repository to deploy the Node application.
4. Add Environment Variables in Railway (`PORT`, `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_PORT`, `JWT_SECRET`).
5. Run the `database/schema.sql` in the Railway MySQL database to instantiate tables and seed data.
6. The app will build using `npm install` and run using `npm start`.
