# coding=utf-8
__author__ = 'Maojun Wang'
#data@:2018-11-14
import paramiko
import sys
import os
import select
from contextlib import contextmanager
from basic_lib.dec_log.log import Log
sys.path.append('...')
'''
import tty, termios      This can only working in UNIX os, not Linux or Windows

https://www.cnblogs.com/yjt1993/p/11239958.html
paramiko是用python语言写的一个模块，遵循self.ssh2协议，支持以加密和认证的方式，进行远程服务器的连接。
paramiko包含两个核心组件：SSHClient和SFTPClient。
SSHClient的作用类似于Linux的ssh命令，是对SSH会话的封装，该类封装了传输(Transport)，通道(Channel)及SFTPClient建立的方法(open_sftp)，通常用于执行远程命令。
SFTPClient的作用类似与Linux的sftp命令，是对SFTP客户端的封装，用以实现远程文件操作，如文件上传、下载、修改文件权限等操作。
# Paramiko中的几个基础名词：
1、Channel：是一种类Socket，一种安全的SSH传输通道；
2、Transport：是一种加密的会话，使用时会同步创建了一个加密的Tunnels(通道)，这个Tunnels叫做Channel；
3、Session：是client与Server保持连接的对象，用connect()/start_client()/start_server()开始会话。

文档：代码示例.note
链接：http://note.youdao.com/noteshare?id=9a8d7680df734864b4f2ce50bc7a7109&sub=71F33DFDEFF54DEDABC3F2DDB16481E0
'''
module = __import__('time')
# module.sleep(2)


def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            Log.warning('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator


class Sshlib:
    def __init__(self, hostname, port, username, password, sshtype='CLI'):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.sshtype = sshtype
        self.ssh = None
        self.sftp = None
        paramiko.util.log_to_file("paramiko.log")

    @contextmanager
    def open_temp_session(self, host, port, user, password, dynamic_password_host=None):
        session = SSHSession(host=host, port=port, user=user, password=password,
                             dynamic_password_host=dynamic_password_host)
        yield session
        session.close()

    @log('self.ssh in process')
    def _login(self):
        """cafe code good sample
        设置连接的远程主机没有本地主机密钥或HostKeys对象时的策略，目前支持三种：
        AutoAddPolicy 自动添加主机名及主机密钥到本地HostKeys对象，不依赖load_system_host_key的配置。
        即新建立ssh连接时不需要再输入yes或no进行确认
        WarningPolicy 用于记录一个未知的主机密钥的python警告。并接受，功能上和AutoAddPolicy类似，但是会提示是新连接
        RejectPolicy 自动拒绝未知的主机名和密钥，依赖load_system_host_key的配置。此为默认选项
        """
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password,
                             allow_agent=True)
            Log.info("self.ssh session login complete (sid=%s,host=%s)" % (self.hostname, self.port))
        except Exception:
            raise Exception("sid=%s, host=%s" % (self.hostname, self.port))

        finally:
            pass
        return self.ssh

    def linux(self):
        transport = paramiko.Transport((self.hostname, self.port))
        transport.connect(username=self.username, password=self.password)
        self.ssh = paramiko.SSHClient()
        self.ssh._transport = transport
        return self.ssh

    def security(self):
        """指定本地的RSA私钥文件,如果建立密钥对时设置的有密码，password为设定的密码，如无不用指定password参数
        建立连接, 允许将信任的主机自动加入到known_hosts列表, 指定密钥连接
        """
        pkey = paramiko.RSAKey.from_private_key_file('id_rsa_1024')
        self.ssh = paramiko.self.sshClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname='172.16.32.129', port=2323, username='root', pkey=pkey)
        return self.ssh

    def clisecurity(self):
        """指定本地的RSA私钥文件,如果建立密钥对时设置的有密码，password为设定的密码，如无不用指定password参数
        创建transport对象绑定主机和端口，指定用户和密钥连接, 类属性赋值, 允许将信任的主机自动加入到known_hosts列表
        """
        pkey = paramiko.RSAKey.from_private_key_file('id_rsa_1024')
        transport = paramiko.Transport((self.hostname, self.port))
        transport.connect(username='root', pkey=pkey)
        self.ssh = paramiko.SSHClient()
        self.ssh._transport = transport
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        return self.ssh

    def sftp(self):
        """SFTPCLient作为一个sftp的客户端对象，根据ssh传输协议的sftp会话，实现远程文件操作，如上传、下载、权限、状态
        from_transport(cls,t) 创建一个已连通的SFTP客户端通道
        put(localpath, remotepath, callback=None, confirm=True) 将本地文件上传到服务器
        参数confirm：是否调用stat()方法检查文件状态，返回ls -l的结果
        get(remotepath, localpath, callback=None) 从服务器下载文件到本地
        mkdir() 在服务器上创建目录
        remove() 在服务器上删除目录
        rename() 在服务器上重命名目录
        stat() 查看服务器文件状态
        listdir() 列出服务器目录下的文件

        实例化transport对象，并建立连接, 实例化sftp对象，指定连接对象
        """
        self.ssh = paramiko.Transport((self.hostname, self.port))
        self.ssh.connect(username='root', password='123.com')
        self.sftp = paramiko.SFTPClient.from_transport(transport)
        self.sftp.put(localpath='id_rsa_1024', remotepath='/root/idrsa1024.txt')
        self.sftp.get(remotepath='/root/idrsa1024.txt', localpath='idrsa1024_back.txt')
        return self.ssh

    def login(self, sshtype='CLI'):
        self.ssh = None
        if sshtype == 'CLI':
            self._login()
        elif self.sshtype == 'LINUX':
            print('LINUX')
            self.linux()
        elif self.sshtype == 'security':
            """以上需要确保被访问的服务器对应用户.self.ssh目录下有authorized_keys文件，
            也就是将服务器上生成的公钥文件保存为authorized_keys。并将私钥文件作为paramiko的登陆密钥
            """
            self.security()
        elif self.sshtype == 'clisecurity':
            """必须先将公钥文件传输到服务器的~/.self.ssh/authorized_keys中"""
            self.clisecurity()
        elif self.sshtype == 'SFTP':
            self.sftp()
        elif self.sshtype == 'xshell':
            """建立一个socket, 启动一个客户端
            如果使用rsa密钥登录的话:
            default_key_file = os.path.join(os.environ['HOME'], '.self.ssh', 'id_rsa')
            prikey = paramiko.RSAKey.from_private_key_file(default_key_file)
            trans.auth_publickey(username='super', key=prikey)
            """
            trans = paramiko.Transport(('192.168.2.129', 22))
            trans.start_client()
            trans.auth_password(username='super', password='super')
            """打开一个通道, 获取终端"""
            channel = trans.open_session()
            channel.get_pty()
            # 激活终端，这样就可以登录到终端了，就和我们用类似于xshell登录系统一样
            channel.invoke_shell()
            # 下面就可以执行你所有的操作，用select实现
            # 对输入终端sys.stdin和 通道进行监控,
            # 当用户在终端输入命令后，将命令交给channel通道，这个时候sys.stdin就发生变化，select就可以感知
            # channel的发送命令、获取结果过程其实就是一个socket的发送和接受信息的过程
            while True:
                readlist, writelist, errlist = select.select([channel, sys.stdin, ], [], [])
                # 如果是用户输入命令了,sys.stdin发生变化
                if sys.stdin in readlist:
                    # 获取输入的内容
                    input_cmd = sys.stdin.read(1)
                    # 将命令发送给服务器
                    channel.sendall(input_cmd)

                # 服务器返回了结果,channel通道接受到结果,发生变化 select感知到
                if channel in readlist:
                    # 获取结果
                    result = channel.recv(1024)
                    # 断开连接后退出
                    if len(result) == 0:
                        print("\r\n**** EOF **** \r\n")
                        break
                    # 输出到屏幕
                    sys.stdout.write(result.decode())
                    sys.stdout.flush()

            # 关闭通道
            channel.close()
            # 关闭链接
            trans.close()
        elif self.sshtype == 'xshellteminate':
            ''' This can only working in UNIX os, not Linux or Windows
            实现一个xshell登录系统的效果，登录到系统就不断输入命令同时返回结果
            支持自动补全，直接调用服务器终端
            '''
            # 建立一个socket
            trans = paramiko.Transport(('192.168.2.129', 22))
            # 启动一个客户端
            trans.start_client()
            # 如果使用rsa密钥登录的话
            '''
            default_key_file = os.path.join(os.environ['HOME'], '.self.ssh', 'id_rsa')
            prikey = paramiko.RSAKey.from_private_key_file(default_key_file)
            trans.auth_publickey(username='super', key=prikey)
            '''
            # 如果使用用户名和密码登录
            trans.auth_password(username='super', password='super')
            # 打开一个通道
            channel = trans.open_session()
            # 获取终端
            channel.get_pty()
            # 激活终端，这样就可以登录到终端了，就和我们用类似于xshell登录系统一样
            channel.invoke_shell()

            # 获取原操作终端属性
            oldtty = termios.tcgetattr(sys.stdin)
            try:
                # 将现在的操作终端属性设置为服务器上的原生终端属性,可以支持tab了
                tty.setraw(sys.stdin)
                channel.settimeout(0)

                while True:
                    readlist, writelist, errlist = select.select([channel, sys.stdin, ], [], [])
                    # 如果是用户输入命令了,sys.stdin发生变化
                    if sys.stdin in readlist:
                        # 获取输入的内容，输入一个字符发送1个字符
                        input_cmd = sys.stdin.read(1)
                        # 将命令发送给服务器
                        channel.sendall(input_cmd)

                    # 服务器返回了结果,channel通道接受到结果,发生变化 select感知到
                    if channel in readlist:
                        # 获取结果
                        result = channel.recv(1024)
                        # 断开连接后退出
                        if len(result) == 0:
                            print("\r\n**** EOF **** \r\n")
                            break
                        # 输出到屏幕
                        sys.stdout.write(result.decode())
                        sys.stdout.flush()
            finally:
                # 执行完后将现在的终端属性恢复为原操作终端属性
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

            # 关闭通道
            channel.close()
            # 关闭链接
            trans.close()
        return self.ssh

    # @log('self.ssh in process')
    def sshclient_execmd(self, execmd):
        com = ''
        cm = []
        for command in execmd.splitlines():
            cm += [command.strip()]
            com = ';'.join(cm)
        Log.success(com)
        stdin, stdout, stderr = self.ssh.exec_command(com.encode('ascii'), get_pty=True)
        # stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.
        print(stdout.read().decode(encoding='utf-8'))

    @staticmethod
    def withopen(filename):
        with open(filename, 'rt') as f:
            comm = ''
            for lineno, line in enumerate(f, 1):
                for command in line.split(','):
                    comm += command
            print('command: ', comm)
        return comm

    def __del__(self):
        self.ssh.close()


@log("start to running")
def main():
    hostname = '10.245.46.208'
    port = 22
    sshtype = ['CLI', 'LINUX']
    sshtype = sshtype[1]
    username = ''
    password = ''
    filename = ''
    if sshtype == 'CLI':
        username = 'sysadmin'
        password = 'seanwang'
        filename = 'cmd.txt'
    elif sshtype == 'LINUX':
        username = 'root'
        password = 'root'
        filename = 'shell.txt'

    sh = Sshlib(hostname, port, username, password, sshtype='LINUX')
    execmd = sh.withopen(filename)
    sh.login(sshtype)
    Log.context('execmd: {}'.format(execmd) + '\r')
    sh.sshclient_execmd(execmd)


if __name__ == "__main__":
    main()