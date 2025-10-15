const express = require('express');
const mysql = require('mysql2/promise');
const path = require('path');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static frontend files from /public
app.use(express.static(path.join(__dirname, 'public')));

// ===== CONFIG =====
const PORT = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET || 'change_this_secret';
const SALT_ROUNDS = 10;

// ===== MySQL Pool =====
const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'Shreyas@2005',
  database: 'shreyas',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
  port: 3306,
});

// ===== Ensure required tables (safe to run) =====
async function ensureTables() {
  const conn = await pool.getConnection();
  try {
    await conn.query(`
      CREATE TABLE IF NOT EXISTS hospital (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        address VARCHAR(255) NOT NULL,
        contact VARCHAR(20),
        email VARCHAR(100) UNIQUE,
        password VARCHAR(255),
        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    `);

    await conn.query(`
      CREATE TABLE IF NOT EXISTS bloodbank (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        address VARCHAR(255) NOT NULL,
        contact VARCHAR(20),
        email VARCHAR(100) UNIQUE,
        password VARCHAR(255),
        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    `);

    await conn.query(`
      CREATE TABLE IF NOT EXISTS donor (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(150),
        contact VARCHAR(20),
        blood_type VARCHAR(10),
        last_donated DATE
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    `);

    await conn.query(`
      CREATE TABLE IF NOT EXISTS blood_requests (
        id INT AUTO_INCREMENT PRIMARY KEY,
        hospital_id INT NOT NULL,
        bloodbank_id INT DEFAULT NULL,
        blood_type VARCHAR(10) NOT NULL,
        quantity INT NOT NULL,
        urgent TINYINT(1) DEFAULT 0,
        status VARCHAR(20) DEFAULT 'pending',
        eta INT DEFAULT NULL,
        request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (hospital_id) REFERENCES hospital(id) ON DELETE CASCADE,
        FOREIGN KEY (bloodbank_id) REFERENCES bloodbank(id) ON DELETE SET NULL
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    `);
  } finally {
    conn.release();
  }
}

ensureTables().catch(err => console.error('Error ensuring tables:', err.message));

// ===== Test DB connectivity =====
app.get('/api/test-db', async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT DATABASE() as db, NOW() as time');
    res.json({ ok: true, database: rows[0].db, time: rows[0].time });
  } catch (err) {
    res.status(500).json({ ok: false, error: err.message });
  }
});

// ===== AUTH ROUTES =====

// Register hospital
app.post('/api/hospital/register', async (req, res) => {
  const { name, address, contact, email, password } = req.body;
  if (!name || !address || !email || !password) {
    return res.status(400).json({ error: 'Missing required fields' });
  }
  try {
    const hashed = await bcrypt.hash(password, SALT_ROUNDS);
    const [result] = await pool.query(
      'INSERT INTO hospital (name, address, contact, email, password) VALUES (?, ?, ?, ?, ?)',
      [name, address, contact || null, email, hashed]
    );
    res.json({ id: result.insertId, message: 'Hospital registered' });
  } catch (err) {
    if (err.code === 'ER_DUP_ENTRY') {
      return res.status(409).json({ error: 'Email already registered' });
    }
    console.error('Hospital register error:', err.message);
    res.status(500).json({ error: 'Database error' });
  }
});

// Login hospital
app.post('/api/hospital/login', async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).json({ error: 'Missing required fields' });
  }
  try {
    const [rows] = await pool.query('SELECT id, password, name FROM hospital WHERE email = ? LIMIT 1', [email]);
    if (!rows.length) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    const user = rows[0];
    const valid = await bcrypt.compare(password, user.password);
    if (!valid) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    const token = jwt.sign({ id: user.id, type: 'hospital', name: user.name }, JWT_SECRET, { expiresIn: '8h' });
    res.json({ token, id: user.id, name: user.name });
  } catch (err) {
    console.error('Hospital login error:', err.message);
    res.status(500).json({ error: 'Database error' });
  }
});

// Register bloodbank
app.post('/api/bloodbank/register', async (req, res) => {
  const { name, address, contact, email, password } = req.body;
  if (!name || !address || !email || !password) {
    return res.status(400).json({ error: 'Missing required fields' });
  }
  try {
    const hashed = await bcrypt.hash(password, SALT_ROUNDS);
    const [result] = await pool.query(
      'INSERT INTO bloodbank (name, address, contact, email, password) VALUES (?, ?, ?, ?, ?)',
      [name, address, contact || null, email, hashed]
    );
    res.json({ id: result.insertId, message: 'Blood bank registered' });
  } catch (err) {
    if (err.code === 'ER_DUP_ENTRY') {
      return res.status(409).json({ error: 'Email already registered' });
    }
    console.error('Bloodbank register error:', err.message);
    res.status(500).json({ error: 'Database error' });
  }
});

// Login bloodbank
app.post('/api/bloodbank/login', async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).json({ error: 'Missing required fields' });
  }
  try {
    const [rows] = await pool.query('SELECT id, password, name FROM bloodbank WHERE email = ? LIMIT 1', [email]);
    if (!rows.length) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    const user = rows[0];
    const valid = await bcrypt.compare(password, user.password);
    if (!valid) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    const token = jwt.sign({ id: user.id, type: 'bloodbank', name: user.name }, JWT_SECRET, { expiresIn: '8h' });
    res.json({ token, id: user.id, name: user.name });
  } catch (err) {
    console.error('Bloodbank login error:', err.message);
    res.status(500).json({ error: 'Database error' });
  }
});

// ===== API ROUTES =====

// Get hospitals
app.get('/api/hospitals', async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT id, name, address, contact FROM hospital');
    res.json(rows);
  } catch (err) {
    console.error('Error fetching hospitals:', err.message);
    res.status(500).json({ error: 'Database error fetching hospitals' });
  }
});

// Get bloodbanks
app.get('/api/bloodbanks', async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT id, name, address, contact FROM bloodbank');
    res.json(rows);
  } catch (err) {
    console.error('Error fetching bloodbanks:', err.message);
    res.status(500).json({ error: 'Database error fetching bloodbanks' });
  }
});

// Get blood requests with optional bloodbank filter
app.get('/api/blood-requests', async (req, res) => {
  const bloodbankId = req.query.bloodbank_id || null;
  try {
    let sql = `
      SELECT br.id, br.hospital_id, br.bloodbank_id, br.blood_type, br.quantity,
             br.urgent, br.status, br.eta, br.request_time,
             h.name AS hospital_name
      FROM blood_requests br
      LEFT JOIN hospital h ON br.hospital_id = h.id
      WHERE 1=1
    `;
    const params = [];
    if (bloodbankId) {
      sql += ' AND br.bloodbank_id = ?';
      params.push(bloodbankId);
    }
    const [rows] = await pool.query(sql, params);
    res.json(rows);
  } catch (err) {
    console.error('Error fetching blood requests:', err.message);
    res.status(500).json({ error: 'Database error fetching blood requests' });
  }
});

// Create blood request
app.post('/api/blood-requests', async (req, res) => {
  const { hospital_id, blood_type, quantity, urgent, bloodbank_id } = req.body;
  if (!hospital_id || !blood_type || !quantity) {
    return res.status(400).json({ error: 'Missing required fields' });
  }
  try {
    const [result] = await pool.query(
      `INSERT INTO blood_requests (hospital_id, blood_type, quantity, urgent, bloodbank_id, status)
       VALUES (?, ?, ?, ?, ?, 'pending')`,
      [hospital_id, blood_type, quantity, urgent ? 1 : 0, bloodbank_id || null]
    );
    res.json({ id: result.insertId, message: 'Request created' });
  } catch (err) {
    console.error('Error creating blood request:', err.message);
    res.status(500).json({ error: 'Database error creating request' });
  }
});

// Accept blood request
app.post('/api/blood-requests/:id/accept', async (req, res) => {
  const id = req.params.id;
  const eta = req.body.eta ?? 30;
  try {
    const [result] = await pool.query(
      'UPDATE blood_requests SET status = ?, eta = ? WHERE id = ? AND status = ?',
      ['accepted', eta, id, 'pending']
    );
    if (result.affectedRows === 0) {
      return res.status(404).json({ error: 'Request not found or not pending' });
    }
    res.json({ message: 'Request accepted', id, eta });
  } catch (err) {
    console.error('Error accepting request:', err.message);
    res.status(500).json({ error: 'Database error accepting request' });
  }
});

// Catch all unknown GETs (for static handled by express.static)
app.get('/*wildcard', (req, res) => {
  res.status(404).send('Not Found');
});



// Start server
app.listen(PORT, () => console.log(`🚀 Server running on http://localhost:${PORT}`));
