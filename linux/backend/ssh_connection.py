import paramiko
import select
import stat
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
        self.sftp = None
        logger.debug(f"SSHConnection instance created for {username}@{hostname}")

    def _load_private_key(self):
        key_classes = (
            paramiko.RSAKey,
            paramiko.Ed25519Key,
            paramiko.ECDSAKey,
            paramiko.DSSKey,
        )
        for key_class in key_classes:
            try:
                return key_class.from_private_key_file(self.key_path)
            except Exception:
                continue
        raise ValueError(f"Unsupported private key format: {self.key_path}")

    def connect(self):
        logger.info(f"Attempting SSH connection to {self.username}@{self.hostname}")
        try:
            if self.key_path:
                logger.debug(f"Using private key authentication: {self.key_path}")
                key = self._load_private_key()
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

    def open_sftp(self):
        if self.sftp:
            return self.sftp
        self.sftp = self.client.open_sftp()
        logger.info(f"SFTP session opened for {self.hostname}")
        return self.sftp

    def list_directory(self, path="."):
        sftp = self.open_sftp()
        entries = []
        for entry in sftp.listdir_attr(path):
            entries.append({
                "name": entry.filename,
                "path": f"{path.rstrip('/')}/{entry.filename}" if path != "/" else f"/{entry.filename}",
                "is_dir": stat.S_ISDIR(entry.st_mode),
                "size": entry.st_size,
                "mtime": entry.st_mtime,
            })
        return sorted(entries, key=lambda item: (not item["is_dir"], item["name"].lower()))

    def normalize_remote_path(self, path="."):
        return self.open_sftp().normalize(path)

    def download_file(self, remote_path, local_path):
        self.open_sftp().get(remote_path, local_path)
        logger.info(f"Downloaded {remote_path} to {local_path}")

    def upload_file(self, local_path, remote_path):
        self.open_sftp().put(local_path, remote_path)
        logger.info(f"Uploaded {local_path} to {remote_path}")

    def close_sftp(self):
        if self.sftp:
            self.sftp.close()
            self.sftp = None
            logger.info(f"SFTP session closed for {self.hostname}")

    def disconnect(self):
        logger.info(f"Disconnecting from {self.hostname}")
        self.close_sftp()
        if self.shell:
            self.shell.close()
        self.client.close()
