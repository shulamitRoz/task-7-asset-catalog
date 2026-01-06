import pytest
from pathlib import Path
import time
from client.watcher import Watcher
from client.uploader import FileUploader

def test_watcher_detects_new_file(tmp_path):
    # משתמשים בתיקייה זמנית
    assets_dir = tmp_path
    uploader = FileUploader()

    # יוצרים את ה-Watcher עם התיקייה הזמנית
    watcher = Watcher(uploader, assets_dir=str(assets_dir))

    # מפעילים את ה-Watcher (מאזין בזמן אמת)
    watcher.observer.start()

    try:
        # יוצרים קובץ חדש בתיקייה
        new_file = assets_dir / "test.txt"
        new_file.write_text("Hello")

        # נותנים ל-Watcher זמן קצר לזהות את הקובץ ולהעלות אותו
        time.sleep(0.5)

        # בודקים שהקובץ נחשב ככפול (כלומר היסטוריית ה־hash עודכנה)
        file_hash = uploader.hash_manager.calculate_hash(str(new_file))
        assert file_hash in uploader.hash_manager.hashes  # <--- כאן התיקון

    finally:
        # עוצרים את ה-Watcher אחרי הבדיקה
        watcher.observer.stop()
        watcher.observer.join()
