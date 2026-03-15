import os
import paramiko
from utils.logger import logger

def generate_ssh_key(path, key_type='RSA', bits=2048):
    """Generate an SSH key pair (Private + Public)."""
    try:
        if key_type == 'RSA':
            key = paramiko.RSAKey.generate(bits)
        elif key_type == 'Ed25519':
            key = paramiko.Ed25519Key.generate()
        else:
            raise ValueError(f"Unsupported key type: {key_type}")

        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Save Private Key
        key.write_private_key_file(path)
        os.chmod(path, 0o600)

        # Save Public Key
        pub_path = f"{path}.pub"
        with open(pub_path, "w") as f:
            f.write(f"{key.get_name()} {key.get_base64()}")

        logger.info(f"SSH Key generated successfully: {path}")
        return path, pub_path
    except Exception as e:
        logger.error(f"Failed to generate SSH key: {e}")
        raise e
