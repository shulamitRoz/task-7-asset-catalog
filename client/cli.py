import os
import typer
from client.uploader import FileUploader
from client.watcher import Watcher

app = typer.Typer()
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
# יוצרים את האובייקטים של המחלקות
uploader = FileUploader()
watcher = Watcher(uploader=uploader, assets_dir=ASSETS_DIR)

@app.command()
def run():
    """Start the watcher to auto-upload files"""
    watcher.start()  

@app.command()
def upload():
    """Upload all files manually"""
    uploader.upload_all()  

@app.command()
def status():
    """Show the current status of files"""
    uploader.status()  
if __name__ == "__main__":
    app()
