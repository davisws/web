import os
import json
import requests
from flask import Flask, redirect, request, session, render_template, url_for

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Nova Bot Dashboard</title>
  <style>
    body {
      margin: 0;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background-color: #0d1117;
      color: #f0f6fc;
    }

    .navbar {
      background-color: #161b22;
      padding: 15px 30px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }

    .navbar h1 {
      margin: 0;
      color: #58a6ff;
    }

    .btn {
      background-color: #238636;
      padding: 10px 20px;
      border: none;
      border-radius: 8px;
      color: white;
      font-weight: bold;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }

    .btn:hover {
      background-color: #2ea043;
    }

    .container {
      padding: 40px;
      max-width: 800px;
      margin: auto;
    }

    .card {
      background-color: #161b22;
      padding: 25px;
      margin: 20px 0;
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }

    .input, textarea {
      width: 100%;
      padding: 10px;
      border-radius: 6px;
      border: none;
      margin: 10px 0;
      background-color: #0d1117;
      color: white;
    }

    textarea {
      resize: vertical;
      min-height: 80px;
    }
  </style>
</head>
<body>
  <div class="navbar">
    <h1>Nova Bot Dashboard</h1>
    <button class="btn" onclick="location.href='/login'">Login with Discord</button>
  </div>

  <div class="container">
    <div class="card">
      <h2>Server Management</h2>
      <p>Once logged in, you'll see all your servers here and can create custom commands.</p>
      <ul id="serverList"></ul>
    </div>

    <div class="card">
      <h2>Create Custom Command</h2>
      <form method="POST" action="/dashboard/server-id">
        <input class="input" name="command" placeholder="Command name (e.g. !hello)" required />
        <textarea class="input" name="response" placeholder="Response to send" required></textarea>
        <button class="btn" type="submit">Save Command</button>
      </form>
    </div>
  </div>
</body>
</html>


if __name__ == "__main__":
    app.run(debug=True)
