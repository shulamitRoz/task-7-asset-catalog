import json
import os
import hashlib

class HashManager:
    def __init__(self, file_path=None):
        self.file_path = file_path or os.path.join(os.path.dirname(__file__), "uploaded_hashes.json")
        self.hashes = self.load_hashes()  # כאן נשמר set של כל ההאשים הקיימים

    def calculate_hash(self, file_path):
        """חשב SHA256 עבור הקובץ"""
        sha = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha.update(chunk)
        return sha.hexdigest()

    def load_hashes(self):
        """טען את ההאשים מהקובץ"""
        if not os.path.exists(self.file_path):
            return set()
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            return set(data)

    def save_hash(self, file_hash):
        """שמור האש חדש"""
        self.hashes.add(file_hash)
        with open(self.file_path, 'w') as f:
            json.dump(list(self.hashes), f)

    def is_duplicate(self, file_path):
        file_hash = self.calculate_hash(file_path)
        if file_hash in self.hashes:
            return True
        self.save_hash(file_hash)
        return False
