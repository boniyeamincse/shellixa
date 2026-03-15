import paramiko

class SSHConnection:
    def __init__(self, hostname, username, password=None, key_path=None):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.key_path = key_path
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        try:
            if self.key_path:
                key = paramiko.RSAKey.from_private_key_file(self.key_path)
                self.client.connect(self.hostname, username=self.username, pkey=key)
            else:
                self.client.connect(self.hostname, username=self.username, password=self.password)
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def execute_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode()

    def disconnect(self):
        self.client.close()
