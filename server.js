
const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

app.post('/schedule', (req, res) => {
  const { name, email, location, date, time, notes } = req.body;

  if (!name || !email || !date || !time) {
    return res.status(400).json({ message: 'Missing required fields.' });
  }

  // Here you could save to a database or process data as needed
  console.log('New schedule received:', req.body);

  res.json({ message: 'Thanks! Your appointment was scheduled.' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log('Server running on http://localhost:' + PORT);
});
