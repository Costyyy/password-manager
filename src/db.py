import sqlite3
import uuid
from datetime import datetime, timezone

DB_PATH = "vault.db"

class Database:
    def __init__(self):
        self.db = self.get_connection()

    def get_connection(self):
        return sqlite3.connect(DB_PATH)

    def init_db(self):
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS entries(
                                  id TEXT PRIMARY KEY,
                                  site TEXT NOT NULL,
                                  username TEXT NOT NULL,
                                  ciphertext BLOB NOT NULL,
                                  nonce BLOB NOT NULL,
                                  updated_at TEXT NOT NULL
                                  );
            CREATE TABLE IF NOT EXISTS vault_meta(
                                  key TEXT PRIMARY KEY,
                                  value BLOB
                                  );
        """)

    def add_entry(self, site, username, ciphertext, nonce):
        entry_id = str(uuid.uuid4())
        updated_at = datetime.now(timezone.utc).isoformat()
        self.db.execute("INSERT INTO entries (id, site, username, ciphertext, nonce, updated_at) VALUES (?, ?, ?, ?, ?, ?)", (entry_id, site, username, ciphertext, nonce, updated_at))

        self.db.commit()

        return entry_id
    
    def get_entry_by_site(self, site):
        cursor = self.db.execute("SELECT * FROM entries WHERE site = ?", (site,))

        return cursor.fetchone()
    
    def get_all_entries(self):
        cursor = self.db.execute("SELECT * FROM entries")

        return cursor.fetchall()
    
    def unpdate_entry(self, site, ciphertext, nonce):
        updated_at = datetime.now(timezone.utc).isoformat()
        self.db.execute("UPDATE entries SET ciphertext = ?, nonce = ?, updated_at = ? WHERE site = ?", (ciphertext, nonce, updated_at, site))

    def delete_entry(self, site):
        self.db.execute("DELETE FROM entries WHERE site = ?", (site, ))

    def get_meta(self, key):
        cursor = self.db.execute("SELECT value FROM vault_meta WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row[0] if row else None
    
    def set_meta(self, key, value):
        self.db.execute("INSERT OR REPLACE INTO vault_meta (key, value) VALUES (?, ?)", (key, value))
