📁 File Upload Client–Server System
🧭 Overview

This project implements a Client–Server file upload system that prevents duplicate uploads using SHA-256 hashing and stores detailed metadata for each uploaded file.
The system is built in Python and demonstrates clean architecture, separation of concerns, and practical use of hashing, CLI tools, and a REST server.

✨ Key Features

📦 Upload files from client to server

🔐 SHA-256 hash calculation

🚫 Duplicate file detection (client & server side)

🗂️ Metadata storage (filename, hash, upload time)

💾 Persistent storage using JSON files

🧪 Test-ready project structure

🖥️ Command Line Interface (CLI)

🖥️ Server Side
server.py
Flask-based HTTP server
Exposes /upload endpoint
Delegates all logic to FileManager
file_manager.py
Central business-logic class responsible for:
Calculating file hashes
Detecting duplicates
Saving files to storage
Storing hashes in hashes.json
Storing metadata in metadata.json
This design keeps the server thin and maintainable.

💻 Client Side
CLI Commands
Run from project root:
python -m client.cli run
Watches the assets directory and uploads new files automatically.

python -m client.cli upload
Manually uploads files.

python -m client.cli status
Displays upload status of each file.

🔁 Duplicate Protection Strategy

Client side: avoids unnecessary uploads by checking local hashes

Server side: final authority — prevents duplicate storage even if client fails

This double-check approach improves performance and reliability.

🧪 Testing

Client tests are implemented

Tests are executed using:

python -m pytest

🚀 Technologies Used

Python 3

Flask

Typer (CLI)

hashlib (SHA-256)

JSON file storage

pytest

📌 Future Improvements

Add full server-side tests

Replace JSON storage with a database

Add authentication / user tracking

Improve error handling and logging
