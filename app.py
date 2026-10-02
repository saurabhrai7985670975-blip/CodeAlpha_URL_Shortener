import sqlite3
import random
import string
from flask import Flask, request, redirect, render_template_string, jsonify

app = Flask(__name__)
DB_FILE = "shortener.db"

# Database setup
def init_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL,
            clicks INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# Helper to generate random 6-character short code
def get_random_code(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))

# Simple frontend UI
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Shortener</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f6f8;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .card {
            background: #ffffff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            width: 380px;
            text-align: center;
        }
        input[type="url"] {
            width: 90%;
            padding: 10px;
            margin-bottom: 12px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .result {
            margin-top: 20px;
            padding: 10px;
            background: #eef9ff;
            border-radius: 4px;
            word-break: break-all;
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>URL Shortener</h2>
        <form method="POST" action="/shorten-form">
            <input type="url" name="url" placeholder="Paste your long URL here..." required>
            <br>
            <button type="submit">Generate Short URL</button>
        </form>

        {% if short_url %}
        <div class="result">
            <p><strong>Short Link:</strong></p>
            <a href="{{ short_url }}" target="_blank">{{ short_url }}</a>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

# Form submission route
@app.route("/shorten-form", methods=["POST"])
def shorten_form():
    long_url = request.form.get("url")
    if not long_url:
        return redirect("/")

    code = get_random_code()

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO links (original_url, short_code) VALUES (?, ?)", (long_url, code))
    conn.commit()
    conn.close()

    short_url = request.host_url + code
    return render_template_string(HTML_PAGE, short_url=short_url)

# API route (JSON format)
@app.route("/api/shorten", methods=["POST"])
def shorten_api():
    payload = request.get_json(silent=True) or {}
    long_url = payload.get("url")

    if not long_url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    code = get_random_code()

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO links (original_url, short_code) VALUES (?, ?)", (long_url, code))
    conn.commit()
    conn.close()

    return jsonify({
        "original_url": long_url,
        "short_url": request.host_url + code,
        "short_code": code
    }), 201

# Redirect route
@app.route("/<short_code>")
def handle_redirect(short_code):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT original_url, clicks FROM links WHERE short_code = ?", (short_code,))
    row = cursor.fetchone()

    if row:
        original_url, clicks = row
        cursor.execute("UPDATE links SET clicks = ? WHERE short_code = ?", (clicks + 1, short_code))
        conn.commit()
        conn.close()
        return redirect(original_url)

    conn.close()
    return "<h3>Error: Short URL not found!</h3>", 404

if __name__ == "__main__":
    init_database()
    app.run(debug=True, port=5000)