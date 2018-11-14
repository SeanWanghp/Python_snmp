# --encoding=UTF-8--
# coding=gbk
__author__ = 'Sewang'
# print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word
# source code:    https://www.shiyanlou.com/courses/?course_type=all&tag=Python&fee=all&page=7
#C:\Python27\Doc python
#data@:2017/4/10
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word

import multiprocessing, telnetlib, paramiko, subprocess, string
import os, sys, logging, datetime, threading
from time import sleep
import re as sre
from multiprocessing import Process


def login(ip, port, name, passw):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port, username=name, password=passw, timeout=10)
    return client


####################This pare only support for linux no switch path

def linux_ssh():
    ip = '10.245.59.200'
    client = login(ip, 22, 'root', 'rootgod')
    cli_steps = '''pwd
                    df
                    ls'''
    if type(cli_steps) is list:
        for cli in cli_steps:
            stdin, stdout, stderr = client.exec_command(cli, get_pty='# ')
            print stdout.readlines()
            for std in stdout.readlines():
                print std
    elif type(cli_steps) is str:
        print '1111'
        for cli in cli_steps.split('\r\n'):
            stdin, stdout, stderr = client.exec_command(cli, get_pty='# ')
            print "aaa:", stdout.readlines()
            for std in stdout.readlines():
                print "bbbb:", std


######################This part will support linux switch to CLI command
def axos_ssh():
    ip = '10.245.46.216'
    client = login(ip, 22, 'root', 'root')
    ssh = client.invoke_shell()
    buff = ''
    enter = "\n"
    while not buff.endswith('~# '):
        resp = ssh.recv(9999)
        buff += resp
    print "buff start:", buff

    cli_steps = '''cli
                    show vlan'''
    buff_cli = ''
    if type(cli_steps) is list:
        for cli in cli_steps:
            ssh.send(cli)
            ssh.send(enter)
            buff = ''
            while not buff.endswith('# '):
                resp = ssh.recv(9999)
                buff += resp
            buff_cli += buff

    elif type(cli_steps) is str:
        for cli in cli_steps.split('\n'):
            ssh.send(cli)
            ssh.send(enter)
            buff = ''
            while not buff.endswith('# '):
                resp = ssh.recv(9999)
                buff += resp
            buff_cli += buff

    print "buff_cli:", buff_cli
    client.close()


#############Threading of SSH
def ssh2(ip, username, passwd, cmd):
    try:
        ssh = login(ip, 22, username, passwd)
        for m in cmd:
            stdin, stdout, stderr = ssh.exec_command(m)
            out = stdout.readlines()
            for o in out:
                print o,  # 屏幕输出
        print '%s\tOK\n' % (ip)
        ssh.close()
    except:
        print '%s\tError\n' % (ip)


def SSH_thread():
    cmd = ['echo hello!']  # 需要执行的命令列表
    username = "root"  # 用户名
    passwd = "root"  # 密码
    threads = []  # 多线程
    print "Begin excute......"
    for i in range(1, 10):
        ip = '192.168.1.' + str(i)
        a = threading.Thread(target=ssh2, args=(ip, username, passwd, cmd))
        a.start()


def log_paramiko(ip, port, user, passw):
    t = paramiko.Transport((ip, port))
    t.connect(username=user, password=passw)
    sftp = paramiko.SFTPClient.from_transport(t)
    return sftp


# ###########  上传文件到远程
def sftp_put(ip, port, user, passw):
    sftp = log_paramiko(ip, port, user, passw)
    remotepath = '/tmp/test.txt'
    localpath = '/tmp/test.txt'
    sftp.put(localpath, remotepath)


###########  从远程下载文件
def sftp_get(ip, port, user, passw):
    sftp = log_paramiko(ip, port, user, passw)
    remotepath='/tmp/test.txt'
    localpath='/tmp/test.txt'
    sftp.get(remotepath, localpath)


##########SSH RUNNING SAMPLE
def paramiko_ss(ip, port, user, passw):
    ssh = login(ip, port, user, passw)
    stdin, stdout, stderr = ssh.exec_command("你的命令")
    print stdout.readlines()
    ssh.close()


if __name__ == '__main__':
    # linux_ssh()
    # axos_ssh()
    SSH_thread()

