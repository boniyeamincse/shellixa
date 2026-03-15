import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from utils.logger import logger

class SecurityManager:
    """Handles AES-256-GCM encryption and master password verification."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SecurityManager, cls).__new__(cls)
            cls._instance.master_key = None
        return cls._instance

    def initialize(self, master_password, salt):
        """Derive the master key from password and salt."""
        try:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            self.master_key = kdf.derive(master_password.encode())
            logger.info("SecurityManager initialized with master key.")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize SecurityManager: {e}")
            return False

    def encrypt(self, plaintext):
        """Encrypt text using AES-256-GCM."""
        if not self.master_key or not plaintext:
            return plaintext
        
        try:
            aesgcm = AESGCM(self.master_key)
            nonce = os.urandom(12)
            ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
            # Combine nonce and ciphertext for storage
            combined = nonce + ciphertext
            return base64.b64encode(combined).decode()
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            return plaintext

    def decrypt(self, encrypted_text):
        """Decrypt text using AES-256-GCM."""
        if not self.master_key or not encrypted_text:
            return encrypted_text
        
        try:
            combined = base64.b64decode(encrypted_text.encode())
            nonce = combined[:12]
            ciphertext = combined[12:]
            aesgcm = AESGCM(self.master_key)
            decrypted = aesgcm.decrypt(nonce, ciphertext, None)
            return decrypted.decode()
        except Exception as e:
            logger.debug(f"Decryption failed or data not encrypted: {e}")
            return encrypted_text # Return as-is if decryption fails (might be unencrypted legacy data)

    @staticmethod
    def hash_password(password, salt):
        """Securely hash a password for storage verification."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return kdf.derive(password.encode())

    @staticmethod
    def generate_salt():
        """Generate a secure random salt."""
        return os.urandom(16)
