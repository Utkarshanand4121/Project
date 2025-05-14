from cryptography.fernet import Fernet
import os

fernet = Fernet(os.getenv("FERNET_KEY"))

def encrypt_id(file_id: str) -> str:
    return fernet.encrypt(file_id.encode()).decode()

def decrypt_id(enc_id: str) -> str:
    return fernet.decrypt(enc_id.encode()).decode()
