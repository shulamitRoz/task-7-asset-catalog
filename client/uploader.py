import os
import requests
import typer
from client.hash_manager import HashManager

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
SERVER_URL = "http://127.0.0.1:5000/upload"

class FileUploader:
    def __init__(self):
        self.assets_dir = ASSETS_DIR
        self.server_url = SERVER_URL
        self.hash_manager = HashManager()

    def upload_file(self, file_path):
        
        relative_path = os.path.relpath(file_path, self.assets_dir)

        if self.hash_manager.is_duplicate(file_path):
            typer.echo(f"- Skipping {relative_path}, duplicate detected.")
            return

        typer.echo(f"- Uploading {relative_path} ...")
        with open(file_path, 'rb') as f:
            try:
                response = requests.post(
                    self.server_url,
                    files={'file': (relative_path, f)}
                )
                if response.status_code == 200:
                    typer.echo(f"{relative_path} uploaded successfully!")
                else:
                    typer.echo(f"Failed to upload {relative_path}: {response.text}")
            except Exception as e:
                typer.echo(f"Error uploading {relative_path}: {e}")          

    def upload_all(self):
        files = os.listdir(self.assets_dir)
        if not files:
            typer.echo("No files to upload in assets folder.")
            return
        for f in files:
            self.upload_file(os.path.join(self.assets_dir, f))

    def status(self):
        files = os.listdir(self.assets_dir)
        if not files:
            typer.echo("No files in assets folder.")
            return

        typer.echo("Files status:")
        for f in files:
            file_path = os.path.join(self.assets_dir, f)
            if self.hash_manager.calculate_hash(file_path) in self.hash_manager.hashes:
                typer.echo(f"- {f}: Uploaded")
            else:
                typer.echo(f"- {f}: New / Not uploaded")
    