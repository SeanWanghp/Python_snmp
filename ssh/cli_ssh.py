# coding=utf-8
#C:\Python27\Doc python
__author__='Sean Wang'
#data@:2018-11-14
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word
from basic_lib.dec_log.log import Log
import paramiko, sys
sys.path.append('...')
'''
paramiko是用python语言写的一个模块，遵循SSH2协议，支持以加密和认证的方式，进行远程服务器的连接。
'''


def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            Log.warning('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator


@log('ssh in process')
def _login(self):
    '''cafe code good sample'''
    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host, self.port, username=self.user, password=self.password,
                    timeout=self.connect_timeout)
        # time.sleep(2.0)

        self._session = ssh
        self.logger.info("ssh session login complete (sid=%s,host=%s)" % (self.sid, self.host))
    except Exception:
        raise SSHLoginException("sid=%s, host=%s" % (self.sid, self.host))

    finally:
        pass


@log('ssh in process')
def sshclient_execmd(hostname, port, username, password, execmd):
    paramiko.util.log_to_file("paramiko.log")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(hostname=hostname, port=port, username=username, password=password)
    for command in execmd.splitlines():
        stdin, stdout, stderr = ssh.exec_command(command.encode('ascii'))
        # stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.
        print(stdout.read().decode(encoding='utf-8'))

    ssh.close()


def with_open(filename):
    with open(filename, 'rt') as f:
        comm = ''
        for lineno, line in enumerate(f, 1):
            for command in line.split(','):
                command.strip()
                comm += command
        print('command: ', comm)
    return comm


@log("start to running")
def main():
    hostname = '10.245.46.208'
    port = 22
    username = 'sysadmin'
    password = 'seanwang'
    filename = 'cmd.txt'
    execmd = with_open(filename)
    sshclient_execmd(hostname, port, username, password, execmd)


if __name__ == "__main__":
    main()