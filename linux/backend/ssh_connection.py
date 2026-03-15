import paramiko
import select
from utils.logger import logger

class SSHConnection:
    def __init__(self, hostname, username, password=None, key_path=None):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.key_path = key_path
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.shell = None
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

    def open_shell(self, term='xterm', width=80, height=24):
        """Invoke an interactive shell session."""
        try:
            self.shell = self.client.invoke_shell(term=term, width=width, height=height)
            self.shell.setblocking(0)
            logger.info(f"Interactive shell opened for {self.hostname}")
            return True
        except Exception as e:
            logger.error(f"Failed to open interactive shell: {e}")
            return False

    def send_command(self, command):
        """Send a command string to the interactive shell."""
        if self.shell:
            self.shell.send(command)
            logger.debug(f"Sent to shell: {command.strip()}")
        else:
            logger.error("No active shell session to send command to")

    def recv_ready(self):
        """Check if data is available to read from the shell."""
        return self.shell and self.shell.recv_ready()

    def receive_output(self, bufsize=1024):
        """Receive output from the interactive shell."""
        if self.shell and self.shell.recv_ready():
            return self.shell.recv(bufsize).decode('utf-8', 'ignore')
        return ""

    def execute_command(self, command):
        """Execute a single command and return its output (standard exec_command)."""
        logger.debug(f"Executing remote command on {self.hostname}: {command}")
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode()

    def disconnect(self):
        logger.info(f"Disconnecting from {self.hostname}")
        if self.shell:
            self.shell.close()
        self.client.close()
