import paramiko, logging
import sys
sys.path.append('...')
from basic_lib.decorator.log import Log

def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            Log.warning('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

def sshclient_execmd(hostname, port, username, password, execmd):
    paramiko.util.log_to_file("paramiko.log")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(hostname=hostname, port=port, username=username, password=password)
    for command in execmd.splitlines():
        stdin, stdout, stderr = ssh.exec_command(command)
        # stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.

        print stdout.read()

    ssh.close()

@log("start to running")
def main():
    hostname = '10.245.46.208'
    port = 22
    username = 'sysadmin'
    password = 'sysadmin'
    execmd = '''paginate false
                show card
                show version
                show igmp
                show vlan
                show interface summary'''

    sshclient_execmd(hostname, port, username, password, execmd)


if __name__ == "__main__":
    main()