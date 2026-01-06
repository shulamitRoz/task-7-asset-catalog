# tests/test_uploader.py
import os
from unittest.mock import patch
from client.uploader import FileUploader

def test_upload_skips_duplicates(tmp_path):
    file1 = tmp_path / "file1.txt"
    file1.write_text("Hello")

    uploader = FileUploader()
    uploader.hash_manager.hashes = set()  # <--- תוקן כאן

    # מגרילים שהקובץ הועלה פעם ראשונה
    with patch("requests.post") as mock_post:
        uploader.upload_file(str(file1))
        assert mock_post.called

    # עכשיו הכפלה - אין קריאה ל-post
    with patch("requests.post") as mock_post:
        uploader.upload_file(str(file1))
        assert not mock_post.called
