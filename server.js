const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const DATA_FILE = path.join(__dirname, 'appointments.json');

// Ensure appointments.json exists and is writable
try {
  if (!fs.existsSync(DATA_FILE)) {
    fs.writeFileSync(DATA_FILE, '[]', 'utf-8');
    console.log('Created new appointments.json');
  }

  fs.appendFileSync(DATA_FILE, ''); // test write permission
  console.log('Using file:', DATA_FILE);
} catch (err) {
  console.error('❌ Cannot access or write to appointments.json:', err);
  process.exit(1);
}

// Serve the HTML form
app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>Lawn Labor Solutions - Book Quote</title>
      <style>
        body { font-family: Arial; background: #e8f5e9; margin: 0; padding: 0; }
        .container {
          max-width: 500px; margin: 50px auto; background: white;
          padding: 30px; border-radius: 10px;
          box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #2e7d32; text-align: center; }
        label { margin-top: 15px; display: block; font-weight: bold; }
        input, textarea, button {
          width: 100%; padding: 10px; margin-top: 5px;
          border: 1px solid #ccc; border-radius: 5px;
        }
        button {
          background: #43a047; color: white;
          border: none; cursor: pointer;
          margin-top: 20px;
        }
        button:hover { background: #388e3c; }
        #responseMessage { margin-top: 15px; text-align: center; font-weight: bold; }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>Schedule Lawn Care</h1>
        <form id="form">
          <label>Name:</label>
          <input type="text" name="name" required />
          <label>Email:</label>
          <input type="email" name="email" required />
          <label>Location:</label>
          <input type="text" name="location" required />
          <label>Date:</label>
          <input type="date" name="date" required />
          <label>Time:</label>
          <input type="time" name="time" required />
          <label>Notes:</label>
          <textarea name="notes" rows="3"></textarea>
          <button type="submit">Book Now</button>
        </form>
        <p id="responseMessage"></p>
      </div>
      <script>
        document.getElementById('form').addEventListener('submit', async (e) => {
          e.preventDefault();
          const form = e.target;
          const data = Object.fromEntries(new FormData(form).entries());

          const res = await fetch('/schedule', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
          });

          const result = await res.json();
          document.getElementById('responseMessage').textContent = result.message;
          form.reset();
        });
      </script>
    </body>
    </html>
  `);
});

// Handle appointment booking
app.post('/schedule', (req, res) => {
  console.log('📥 Received POST at /schedule');
  console.log('➡️ Data:', req.body);

  const { name, email, location, date, time, notes } = req.body;

  if (!name || !email || !location || !date || !time) {
    console.warn('⚠️ Missing required fields');
    return res.status(400).json({ message: 'Missing required fields.' });
  }

  const newAppointment = {
    id: Date.now(),
    name,
    email,
    location,
    date,
    time,
    notes
  };

  try {
    const appointments = JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'));
    appointments.push(newAppointment);
    fs.writeFileSync(DATA_FILE, JSON.stringify(appointments, null, 2));
    console.log('✅ Appointment saved:', newAppointment);
    res.json({ message: 'Thanks! Your lawn care quote is scheduled.' });
  } catch (err) {
    console.error('❌ Error saving appointment:', err);
    res.status(500).json({ message: 'Server error saving appointment.' });
  }
});

// Optional: View all appointments
app.get('/appointments', (req, res) => {
  try {
    const data = fs.readFileSync(DATA_FILE, 'utf-8');
    res.type('json').send(data);
  } catch (err) {
    console.error('❌ Error reading appointments:', err);
    res.status(500).json({ message: 'Could not load appointments.' });
  }
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🌿 Lawn Labor Solutions running at http://localhost:${PORT}`);
});

/*
📌 Manual test:
curl -X POST http://localhost:3000/schedule \\
  -H "Content-Type: application/json" \\
  -d '{"name":"Test","email":"test@example.com","location":"123 Lane","date":"2025-08-01","time":"10:00","notes":"Testing"}'
*/

