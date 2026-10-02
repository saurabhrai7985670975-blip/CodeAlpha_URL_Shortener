# CodeAlpha URL Shortener

A lightweight backend service built using Python and Flask to shorten long URLs and automatically redirect users to the original destination.

## Features
- Generates a unique 6-character alphanumeric code for each URL.
- Persistent SQLite database storage.
- HTTP Redirection to the destination link.
- Click count tracking.
- Interactive web interface + REST API endpoint (`/api/shorten`).

## Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLite3
- **Frontend:** Minimal HTML/CSS

## Setup & Running Locally

1. Clone this repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/CodeAlpha_URL_Shortener.git](https://github.com/YOUR_USERNAME/CodeAlpha_URL_Shortener.git)
   cd CodeAlpha_URL_Shortener