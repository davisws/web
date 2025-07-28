
const express = require('express');
const nodemailer = require('nodemailer');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

app.post('/schedule', async (req, res) => {
  const { name, email, location, date, time, notes } = req.body;

  const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: process.env.EMAIL_USERNAME,
      pass: process.env.EMAIL_PASSWORD
    }
  });

  const mailOptions = {
    from: email,
    to: process.env.EMAIL_USERNAME,
    subject: 'New Lawn Service Booking',
    text: `
New Booking Request:
Name: ${name}
Email: ${email}
Location: ${location}
Date: ${date}
Time: ${time}
Notes: ${notes || 'None'}
    `
  };

  try {
    await transporter.sendMail(mailOptions);
    res.json({ message: 'Thanks! Your appointment was scheduled.' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'There was an error sending the email.' });
  }
});

app.listen(3000, () => console.log('Server running on http://localhost:3000'));
