const express = require('express');
const session = require('express-session');
const http = require('http');
const path = require('path');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.urlencoded({ extended: true }));

app.use(session({
  secret: 'your-secret-key',
  resave: false,
  saveUninitialized: false,
}));

// Simple in-memory users - replace with real DB in production
const users = {
  Blake: '834bl',
  Davis: '241da',
};

// Middleware to protect dashboard route
function authRequired(req, res, next) {
  if (req.session.username) {
    next();
  } else {
    res.redirect('/login');
  }
}

// Serve static files (for frontend HTML/CSS/JS)
app.use(express.static(path.join(__dirname, 'public')));

// Login page
app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'public/login.html'));
});

// Handle login POST
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  if (users[username] && users[username] === password) {
    req.session.username = username;
    res.redirect('/dashboard');
  } else {
    res.send('Invalid username or password. <a href="/login">Try again</a>');
  }
});

// Dashboard page (chat)
app.get('/dashboard', authRequired, (req, res) => {
  res.sendFile(path.join(__dirname, 'public/dashboard.html'));
});

// Logout
app.get('/logout', (req, res) => {
  req.session.destroy(() => {
    res.redirect('/login');
  });
});

// Socket.IO real-time chat
io.use((socket, next) => {
  let session = socket.request.session;
  if (session && session.username) {
    next();
  } else {
    next(new Error('Unauthorized'));
  }
});

io.on('connection', (socket) => {
  const username = socket.handshake.query.username || 'Anonymous';

  console.log(username + ' connected');

  socket.on('chat message', (msg) => {
    io.emit('chat message', { user: username, message: msg });
  });

  socket.on('disconnect', () => {
    console.log(username + ' disconnected');
  });
});

// Share express-session with socket.io
const sharedSession = require('express-socket.io-session');
io.use(sharedSession(session({
  secret: 'your-secret-key',
  resave: false,
  saveUninitialized: false,
})));

// Start server
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
