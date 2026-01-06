# tests/test_hash_manager.py
import os
import tempfile
from client.hash_manager import HashManager

def test_hash_saves_and_detects_duplicates():
    # יצירת קובץ זמני
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"Hello World")
        tmp_path = tmp.name

    manager = HashManager("test_uploaded.json")

    # בהתחלה אין כפילות
    assert manager.is_duplicate(tmp_path) == False

    # עכשיו זה צריך להיחשב כפול
    assert manager.is_duplicate(tmp_path) == True

    # ניקוי קובץ בדיקה
    os.remove(tmp_path)
    os.remove("test_uploaded.json")
