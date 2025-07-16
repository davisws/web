// server.js - Node.js Express server with Employee Dashboard and Calendar

const express = require("express");
const session = require("express-session");
const http = require("http");
const path = require("path");
const fs = require("fs");
const { Server } = require("socket.io");

const app = express();
const server = http.createServer(app);
const io = new Server(server);

// Express and Session Setup
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

const sessionMiddleware = session({
  secret: "your-secret-key",
  resave: false,
  saveUninitialized: false,
});

app.use(sessionMiddleware);

// Socket.IO session sharing (manual solution for now)
io.use((socket, next) => {
  sessionMiddleware(socket.request, {}, next);
});

// In-memory user store
const users = {
  Blake: "834bl",
};

// Auth middleware
function authRequired(req, res, next) {
  if (req.session.username && users[req.session.username]) {
    next();
  } else {
    res.redirect("/login");
  }
}

// Serve static frontend files
app.use(express.static(path.join(__dirname, "public")));

// Event storage (basic JSON file)
let events = [];
const eventsFile = path.join(__dirname, "data", "events.json");

function loadEvents() {
  if (fs.existsSync(eventsFile)) {
    events = JSON.parse(fs.readFileSync(eventsFile));
  }
}

function saveEvents() {
  fs.writeFileSync(eventsFile, JSON.stringify(events, null, 2));
}

loadEvents();

// Routes
app.get("/login", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "login.html"));
});

app.post("/login", (req, res) => {
  const { username, password } = req.body;
  if (users[username] && users[username] === password) {
    req.session.username = username;
    res.redirect("/dashboard");
  } else {
    res.send("Invalid login. <a href='/login'>Try again</a>");
  }
});

app.get("/logout", (req, res) => {
  req.session.destroy(() => {
    res.redirect("/login");
  });
});

app.get("/dashboard", authRequired, (req, res) => {
  res.sendFile(path.join(__dirname, "public", "dashboard.html"));
});

// REST API for calendar events
app.get("/api/events", authRequired, (req, res) => {
  res.json(events);
});

app.post("/api/events", authRequired, (req, res) => {
  const { title, start, end } = req.body;
  if (!title || !start) {
    return res.status(400).json({ error: "Title and start date required" });
  }
  const newEvent = { id: Date.now(), title, start, end };
  events.push(newEvent);
  saveEvents();
  res.json(newEvent);
});

app.delete("/api/events/:id", authRequired, (req, res) => {
  const id = parseInt(req.params.id);
  events = events.filter((e) => e.id !== id);
  saveEvents();
  res.json({ success: true });
});

// Tawk.to Embed Script Injection
const tawkToScript = `<!--Start of Tawk.to Script--><script type=\"text/javascript\">var Tawk_API=Tawk_API||{},Tawk_LoadStart=new Date();(function(){var s1=document.createElement(\"script\"),s0=document.getElementsByTagName(\"script\")[0];s1.async=true;s1.src='https://embed.tawk.to/68780da23606072bf84a2d97/1j0afagrk';s1.charset='UTF-8';s1.setAttribute('crossorigin','*');s0.parentNode.insertBefore(s1,s0);})();</script><!--End of Tawk.to Script-->`;

app.get("/", (req, res) => {
  const indexPath = path.join(__dirname, "public", "index.html");
  fs.readFile(indexPath, "utf8", (err, data) => {
    if (err) return res.status(500).send("Error loading page");
    res.send(data.replace("</body>", `${tawkToScript}</body>`));
  });
});

// Socket.IO Chat
io.on("connection", (socket) => {
  const username = socket.request.session.username || "Guest";
  console.log(`${username} connected`);

  socket.on("chat message", (msg) => {
    io.emit("chat message", { user: username, message: msg });
  });

  socket.on("disconnect", () => {
    console.log(`${username} disconnected`);
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
