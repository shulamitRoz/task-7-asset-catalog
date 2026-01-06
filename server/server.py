from flask import Flask, request
import os

from .file_manager import FileManager

app = Flask(__name__)

file_manager = FileManager()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {"status": "error", "message": "No file part"}, 400

    file = request.files['file']
    if file.filename == '':
        return {"status": "error", "message": "No selected file"}, 400

    result, status = file_manager.save_file(file)
    return result, status

if __name__ == "__main__":
    app.run(port=5000)
