from SSHLibrary import SSHLibrary

class SshLibrary(SSHLibrary):
    def __init__(self):
        pass

    @classmethod
    def ssh_(self, host, user, password):
        self.ssh = SSHLibrary(timeout=10)
        try:
            self.ssh.open_connection(host)
            self.ssh.login(user, password)
            command = ['show card', 'paginate false', 'show run vlan', 'show version']
            self.session_command(command)
        except ValueError as e:
                raise e
        return self.ssh

    @classmethod
    def session_command(self, command):
        print ("command: ", type(command), command)

        if isinstance(command, list):
            for com in command:
                self.ssh.write(com.encode('ascii'))
                result = self.ssh.read_until('# ')
            return result
        if isinstance(command, str):
            self.ssh.write(command.encode('ascii'))
            result = self.ssh.read_until('# ')
            return result
        else:
            raise RuntimeError('command type error')

    @classmethod
    def reconnection(self, host):
        if self.ssh:
            return self.ssh
        else:
            self.ssh.open_connection(host)
            self.ssh.login(b'sysadmin', b'seanwang')
            return self.ssh


    def __del__(self):
        return self.ssh.close_connection()