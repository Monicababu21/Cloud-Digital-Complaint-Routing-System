const mysql = require('mysql2/promise');
const dotenv = require('dotenv');
const path = require('path');

dotenv.config({ path: path.join(__dirname, '../.env') });
if (!process.env.DB_NAME) {
    dotenv.config({ path: path.join(__dirname, '../../.env') });
}

const pool = mysql.createPool({
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || '',
    database: process.env.DB_NAME || 'complaint_routing',
    port: process.env.DB_PORT || 3306,
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

// Test database connection on startup
pool.getConnection()
    .then(conn => {
        console.log('✅ Database connected successfully!');
        conn.release();
    })
    .catch(err => {
        console.error('❌ Database connection failed:');
        console.error('   Code:', err.code);
        console.error('   Message:', err.message);
        console.error('   Please check your .env file and ensure MySQL is running.');
    });

module.exports = pool;
