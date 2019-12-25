# coding=utf-8
# Date ：2019/12/25 8:37
__author__ = 'Maojun'
import re
import urllib.request
import gzip
import requests
import paramiko
import sys
import os
import select
from time import sleep
from contextlib import contextmanager
from basic_lib.dec_log.log import Log


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
        self.sf = None
        paramiko.util.log_to_file("paramiko.log")

    @log('self.ssh in process')
    def _login(self):
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

    def sftp(self):
        self.ssh = paramiko.Transport((self.hostname, self.port))
        self.ssh.connect(username=self.username, password=self.password)
        self.sf = paramiko.SFTPClient.from_transport(self.ssh)
        # self.sftp.put(localpath='id_rsa_1024', remotepath='/root/idrsa1024.txt')
        self.sf.get(remotepath='/home/caxxx/zhulin/create_dashboard/sean.sh', localpath='sean.sh')
        return self.ssh

    def login(self, sshtype='CLI'):
        self.ssh = None
        if sshtype == 'CLI':
            self._login()
        elif self.sshtype == 'LINUX':
            print('LINUX')
            self.linux()
        elif self.sshtype == 'SFTP':
            self.sftp()
        return self.ssh

    # @log('self.ssh in process')
    def sshclient_execmd(self, execmd, ip, dev_type):
        com = ''
        cm = []
        for command in execmd.splitlines():
            cm += [command.strip()]
            com = ';'.join(cm)
        Log.success(com)
        stdin, stdout, stderr = self.ssh.exec_command(com.encode('ascii'), get_pty='$ ')
        print(stdout.read().decode(encoding='utf-8'))

        # add_device = '/home/caxxx/zhulin/create_dashboard/sean.sh {} "{}"'.format(ip, device_type)
        add_device = 'cd /home/caxxx/zhulin/create_dashboard/\npwd\n./create_dashboard.sh {} "{}"'.format(ip, dev_type)
        print(add_device)
        stdin, stdout, stderr = self.ssh.exec_command(add_device.encode('ascii'), get_pty=True)
        sleep(2)
        result = stdout.read().decode(encoding='utf-8')
        Log.info(result)
        if 'success' in result:
            Log.warning('device add successfully.........')
        elif 'exist' in result:
            Log.warning('device alread exists........')
        else:
            Log.warning('device add failed...........')

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


@log("try to add device to GRAFNA...................")
def main(device_ip):
    hostname = '10.245.251.56'
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
        username = 'caxxx'
        password = 'caxxx123'
        filename = 'shell.txt'

    sh = Sshlib(hostname, port, username, password, sshtype='LINUX')
    execmd = sh.withopen(filename)
    sh.login(sshtype)
    Log.context('execmd: {}'.format(execmd) + '\r')
    sh.sshclient_execmd(execmd, device_ip, dev_type='E7')


class Urlopenlib:
    def __init__(self):
        self.response = None
        pass

    def __del__(self):
        if self.response:
            self.response.close()
        else:
            pass

    def getHtml(self, url):
        """response.info()  web respond head content and check the code mode 'utf-8' or 'gbk'"""
        print(url)
        response = urllib.request.urlopen(url)
        print('head: ', response.info())
        b = response.read()
        if response.getcode() is 200:
            for bb in [b.decode('utf-8')]:
                if bb:
                    print('grafna content: {}'.format(bb))
                else:
                    pass
        return b

    def writeFile(self, fileName, data):
        # 打开文件方式为'a'可不覆盖原有数据
        htmlFile = open(fileName, 'a')
        htmlFile.write(data)
        htmlFile.close()


if __name__ == "__main__":
    device_ip = '10.245.46.216'
    main(device_ip)
    print('please wait for few seconds...............')
    sleep(3)
    # ur = Urlopenlib()
    # url = 'http://10.245.251.173:3001/d/n5xciXfZk/10-245-46-227'
    # # ur.getHtml(url)
    # ur.basicget(url)

