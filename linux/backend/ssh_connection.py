import paramiko
from utils.logger import logger

class SSHConnection:
    def __init__(self, hostname, username, password=None, key_path=None):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.key_path = key_path
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        logger.debug(f"SSHConnection instance created for {username}@{hostname}")

    def connect(self):
        logger.info(f"Attempting SSH connection to {self.username}@{self.hostname}")
        try:
            if self.key_path:
                logger.debug(f"Using private key authentication: {self.key_path}")
                key = paramiko.RSAKey.from_private_key_file(self.key_path)
                self.client.connect(self.hostname, username=self.username, pkey=key)
            else:
                logger.debug("Using password authentication")
                self.client.connect(self.hostname, username=self.username, password=self.password)
            logger.info(f"Successfully connected to {self.hostname}")
            return True
        except Exception as e:
            logger.error(f"Connection to {self.hostname} failed: {e}")
            return False

    def execute_command(self, command):
        logger.debug(f"Executing remote command on {self.hostname}: {command}")
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode()

    def disconnect(self):
        logger.info(f"Disconnecting from {self.hostname}")
        self.client.close()
