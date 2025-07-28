const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
  res.send('Welcome to Lawn Labor Solutions API');
});

app.post('/schedule', (req, res) => {
  const { name, email, location, date, time, notes } = req.body;

  if (!name || !email || !date || !time) {
    return res.status(400).json({ message: 'Missing required fields.' });
  }

  console.log('New schedule received:', req.body);

  res.json({ message: 'Thanks! Your appointment was scheduled.' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log('Server running on http://localhost:' + PORT);
});
