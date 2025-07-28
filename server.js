const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve the HTML form on root "/"
app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>Lawn Labor Solutions</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          background-color: #e8f5e9;
          margin: 0;
          padding: 0;
        }
        .container {
          width: 90%;
          max-width: 500px;
          margin: 50px auto;
          background: white;
          padding: 30px;
          border-radius: 10px;
          box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
          color: #2e7d32;
          text-align: center;
        }
        form {
          display: flex;
          flex-direction: column;
        }
        label {
          margin-top: 15px;
          margin-bottom: 5px;
          font-weight: bold;
        }
        input, textarea, button {
          padding: 10px;
          font-size: 16px;
          border-radius: 5px;
          border: 1px solid #ccc;
        }
        button {
          background-color: #43a047;
          color: white;
          margin-top: 20px;
          cursor: pointer;
          border: none;
          transition: background 0.3s;
        }
        button:hover {
          background-color: #388e3c;
        }
        #responseMessage {
          margin-top: 20px;
          text-align: center;
          font-weight: bold;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>Schedule Lawn Labor</h1>
        <form id="scheduleForm">
          <label>Name:</label>
          <input type="text" name="name" required />

          <label>Email:</label>
          <input type="email" name="email" required />

          <label>Location:</label>
          <input type="text" name="location" />

          <label>Date:</label>
          <input type="date" name="date" required />

          <label>Time:</label>
          <input type="time" name="time" required />

          <label>Notes:</label>
          <textarea name="notes" rows="3"></textarea>

          <button type="submit">Schedule Appointment</button>
        </form>
        <p id="responseMessage"></p>
      </div>
      <script>
        document.getElementById('scheduleForm').addEventListener('submit', async (e) => {
          e.preventDefault();

          const formData = new FormData(e.target);
          const data = Object.fromEntries(formData);

          try {
            const res = await fetch('/schedule', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(data),
            });

            const result = await res.json();
            document.getElementById('responseMessage').textContent = result.message || 'Success!';
            e.target.reset();
          } catch (err) {
            document.getElementById('responseMessage').textContent = 'Error submitting form.';
          }
        });
      </script>
    </body>
    </html>
  `);
});

// Handle form submissions
app.post('/schedule', (req, res) => {
  const { name, email, location, date, time, notes } = req.body;

  if (!name || !email || !date || !time) {
    return res.status(400).json({ message: 'Missing required fields.' });
  }

  console.log('New schedule received:', req.body);

  res.json({ message: 'Thanks! Your appointment was scheduled.' });
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log('Server running at http://localhost:' + PORT);
});
