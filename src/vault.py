import db
import os
import crypto
import merkle

class Vault:
    def __init__(self, master_password):
        self.db = db.Database()
        self.db.init_db()
        salt = self.db.get_meta("salt")
        self.key = None
        # if salt doesn't exist in the vault then generate a new one and save it
        if not salt:
            salt = os.urandom(16)
            self.db.set_meta("salt", salt)
       
        entries = [(data[0], data[3]) for data in self.db.get_all_entries()]
        root = self.db.get_meta("root")
        if root:
            if not merkle.verify(entries, root):
                raise ValueError("Mismatch")
        self.key = crypto.derive_key(master_password, salt)

    def add(self, site, username, password):
        # TO DO: add possiblity to have multiple accounts per website

        if self.db.get_entry_by_site(site):
            self.update(site, password)
            return
        
        ciphertext, nonce = crypto.encrypt(self.key, password)
        self.db.add_entry(site, username, ciphertext, nonce)

        self._update_merkle_root()
    
    def get(self, site):

        data = self.db.get_entry_by_site(site)
        if not data:
            raise ValueError(f"No entry found for {site}")

        try:
            password = crypto.decrypt(self.key, data[3], data[4])
        except:
            raise ValueError("wrong password")
       

        return (data[1], password)
    
    def update(self, site, password):
        if not self.db.get_entry_by_site(site):
            return
        
        ciphertext, nonce = crypto.encrypt(self.key, password)
        self.db.update_entry(site, ciphertext, nonce)

        self._update_merkle_root()

    def delete(self, site):
        if not self.db.get_entry_by_site(site):
            return
        
        self.db.delete_entry(site)

        self._update_merkle_root()

    def list_entries(self):
        return [(data[1], data[2]) for data in self.db.get_all_entries()]
    
    def _update_merkle_root(self):
        entries = [(data[0], data[3]) for data in self.db.get_all_entries()]
        root = merkle.compute_root(entries)
        self.db.set_meta("root", root)
