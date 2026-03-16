from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305 as chacha
from argon2.low_level import hash_secret_raw, Type
import sqlite3
import os




def derive_key(master_password, salt):
    return hash_secret_raw(
    secret=master_password.encode(),
    salt=salt,
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    type=Type.ID
    )

def encrypt(key, plaintext):

    enc = chacha(key)
    nonce = os.urandom(12)

    ciphertext = enc.encrypt(nonce, plaintext.encode(), None)

    return [ciphertext, nonce]


def decrypt(key, ciphertext, nonce):
    
    enc = chacha(key)
    plaintext = enc.decrypt(nonce, ciphertext, None)

    return plaintext

