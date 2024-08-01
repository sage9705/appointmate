# generate_key.py
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key().decode()

if __name__ == "__main__":
    print("Generated key:", generate_key())