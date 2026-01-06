import os
import json
import hashlib
import datetime

class FileManager:
    """
    מנהל קבצים: מחשב hash, בודק כפילויות ושומר מטא-דאטה
    """
    def __init__(self, storage_dir=None, hash_file=None, metadata_file=None):
        self.storage_dir = storage_dir or os.path.join(os.path.dirname(__file__), "server_storage")
        os.makedirs(self.storage_dir, exist_ok=True)

        self.hash_file = hash_file or os.path.join(os.path.dirname(__file__), "hashes.json")
        self.metadata_file = metadata_file or os.path.join(os.path.dirname(__file__), "metadata.json")

        self.hashes = self.load_hashes()
        self.metadata = self.load_metadata()

    # --- HASH FUNCTIONS ---
    def calculate_hash(self, file_path=None, file_obj=None):
        """חשב SHA256 עבור קובץ"""
        sha = hashlib.sha256()
        if file_obj:
            file_obj.seek(0)
            while chunk := file_obj.read(8192):
                sha.update(chunk)
            file_obj.seek(0)
        elif file_path:
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    sha.update(chunk)
        else:
            raise ValueError("Must provide file_path or file_obj")
        return sha.hexdigest()

    def load_hashes(self):
        """טען hash קיימים מקובץ JSON"""
        if not os.path.exists(self.hash_file):
            return set()
        with open(self.hash_file, 'r') as f:
            data = json.load(f)
            return set(data)

    def save_hash(self, file_hash):
        """שמור hash חדש"""
        self.hashes.add(file_hash)
        with open(self.hash_file, 'w') as f:
            json.dump(list(self.hashes), f)

    def is_duplicate(self, file_path=None, file_obj=None):
        """בדוק אם הקובץ כבר קיים לפי hash"""
        file_hash = self.calculate_hash(file_path=file_path, file_obj=file_obj)
        if file_hash in self.hashes:
            return True, file_hash
        return False, file_hash

    # --- METADATA FUNCTIONS ---
    def load_metadata(self):
        """טען מטא-דאטה מקובץ JSON"""
        if not os.path.exists(self.metadata_file):
            return {}
        with open(self.metadata_file, 'r') as f:
            data = json.load(f)
            return data

    def save_metadata(self, filename, file_hash, uploaded_by="anonymous"):
        """שמור מטא-דאטה של קובץ"""
        meta = {
            "filename": filename,
            "hash": file_hash,
            "uploaded_by": uploaded_by,
            "upload_time": datetime.datetime.utcnow().isoformat()
        }
        self.metadata[file_hash] = meta
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=4)

    # --- FILE STORAGE ---
    def save_file(self, file, uploaded_by="anonymous"):
        """
        שמירה של קובץ סופי בשרת, כולל בדיקה כפילות ושמירת מטא-דאטה
        מחזיר: dict עם סטטוס, filename ו-hash
        """
        # בדיקה אם הקובץ קיים
        duplicate, file_hash = self.is_duplicate(file_obj=file)
        if duplicate:
            return {"status": "error", "message": "File already exists (duplicate hash)"}, 409

        # שמירה בקובץ הסופי
        file_path = os.path.join(self.storage_dir, file.filename)
        # יצירת תיקיות אם יש צורך (למשל אם הקובץ בתוך תיקיות משנה)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)

        # שמירת hash ומטא-דאטה
        self.save_hash(file_hash)
        self.save_metadata(file.filename, file_hash, uploaded_by)

        return {"status": "success", "filename": file.filename, "hash": file_hash}, 200
