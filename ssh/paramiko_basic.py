# --encoding=UTF-8--
# coding=gbk
__author__ = 'Maojun'
import paramiko


class Sshclient:
    def __init__(self, host, port, username='root', password='root'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ssh = paramiko.SSHClient()
        """允许连接不在know_hosts文件中的主机"""
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshlogin(self.host, self.port, self.username, self.password)
        self.sshsendcommand()

    def sshlogin(self, host, port, username, password):
        try:
            """设置允许连接known_hosts文件中的主机(默认连接不在known_hosts文件中的主机会拒绝连接抛出SSHException)"""
            self.ssh.connect(host, port, username, password)
        except AuthenticationException:
            logging.warning('username or password error')
            return 1001
        except NoValidConnectionsError:
            logging.warning('connect time out')
            return 1002
        except IOError:
            logging.warning('unknow error')
            print("Unexpected error:", sys.exc_info()[0])
            return 1003
        return 1000

    def sshsendcommand(self):
        stdin, stdout, stderr = self.ssh.exec_command('ls')
        result = stdout.read()
        print(result.decode('utf-8'))
        print('*'*100)

    def __del__(self):
        self.ssh.close()


Sshclient('10.245.59.200', 22, username='root', password='rootgod')


"""second method of paramiko"""
transport = paramiko.Transport(('10.245.46.208', 22))
transport.connect(username='root', password='root')

ssh = paramiko.SSHClient()
ssh._transport = transport

stdin, stdout, stderr = ssh.exec_command('pwd')
print(stdout.read().decode('utf-8'))
transport.close()