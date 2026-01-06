import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import typer
import os

class WatcherHandler(FileSystemEventHandler):
    def __init__(self, uploader):
        self.uploader = uploader

    def on_created(self, event):
        if event.is_directory:
            # העלאת כל הקבצים שבתיקייה שנוצרה
            for root, _, files in os.walk(event.src_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    self.uploader.upload_file(file_path)
        else:
            # קובץ בודד
            self.uploader.upload_file(event.src_path)

    def on_modified(self, event):
        # גם אם הקובץ שונה – מעלים אותו מחדש
        if not event.is_directory:
            self.uploader.upload_file(event.src_path)


class Watcher:
    def __init__(self, uploader, assets_dir):
        self.uploader = uploader
        self.assets_dir = assets_dir
        self.observer = Observer()

    def start(self):
        # הפעלת המעקב על כל תתי-הספריות גם כן
        handler = WatcherHandler(self.uploader)
        self.observer.schedule(handler, self.assets_dir, recursive=True)
        self.observer.start()

        typer.echo(f"Watching directory (including subfolders): {self.assets_dir}")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()

        self.observer.join()
