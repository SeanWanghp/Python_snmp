# --encoding=UTF-8--
# coding=gbk
__author__ = 'Maojun Wang'
# print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word
# source code:      https://www.shiyanlou.com/courses/?course_type=all&tag=Python&fee=all&page=7
#                   http://blog.csdn.net/oatnehc/article/details/46580753
#                   http://www.361way.com/python-paramiko-ssh/3984.html
#C:\Python27\Doc python
#data@:2019/10/25
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word

#!/usr/bin/env python
#coding:utf8
import paramiko


class Sshclient:
    def __init__(self, host, port, username='root', password='root'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        # 创建SSH对象
        self.ssh = paramiko.SSHClient()
        # 允许连接不在know_hosts文件中的主机
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshlogin(self.host, self.port, self.username, self.password)
        self.sshsendcommand()

    def sshlogin(self, host, port, username, password):
        # 连接服务器
        try:
            # 设置允许连接known_hosts文件中的主机（默认连接不在known_hosts文件中的主机会拒绝连接抛出SSHException）
            self.ssh.connect(host, port, username, password)
        except AuthenticationException:
            logging.warning('username or password error')
            return 1001
        except NoValidConnectionsError:
            logging.warning('connect time out')
            return 1002
        except:
            logging.warning('unknow error')
            print("Unexpected error:", sys.exc_info()[0])
            return 1003
        return 1000

    def sshsendcommand(self):
        # 执行命令
        stdin, stdout, stderr = self.ssh.exec_command('ls')
        # 获取命令结果
        result = stdout.read()
        print(result.decode('utf-8'))
        print('*'*100)

    def __del__(self):
        # 关闭连接
        self.ssh.close()


Sshclient('10.245.59.200', 22, username='root', password='rootgod')



##########second method of paramiko
transport = paramiko.Transport(('10.245.46.208', 22))
transport.connect(username='root', password='root')

ssh = paramiko.SSHClient()
ssh._transport = transport

stdin, stdout, stderr = ssh.exec_command('pwd')
print(stdout.read().decode('utf-8'))

transport.close()