# coding=utf-8
# data@:2018-11-14
__author__ = 'Sean Wang'
from try_lib.logging_lib.log import Log
from paramiko import AuthenticationException
from paramiko.client import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import NoValidConnectionsError
import paramiko
import sys
import logging
import threading
import time
sys.path.append('...')
"""paramiko是用python语言写的一个模块，遵循SSH2协议，支持以加密和认证的方式，进行远程服务器的连接。"""


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
    Log.warning("login...................................................")
    for command in execmd.splitlines():
        stdin, stdout, stderr = ssh.exec_command(command)
        """stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction."""
        print(stdout.read().decode(encoding='utf-8'))

    ssh.close()


def with_open(filename):
    with open(filename, 'rt') as f:
        comm = ''
        for lineno, line in enumerate(f, 1):
            for command in line.split(','):
                command.strip()
                comm += command
        print('command: {}'.format(comm))
    return comm


@log("start to running")
def main(ip):
    logging.info("Thread %s: starting", ip)
    hostname = ip
    port = 22
    username = 'sysadmin'
    password = 'seanwang'
    filename = 'cmd.txt'
    execmd = with_open(filename)
    sshclient_execmd(hostname, port, username, password, execmd)
    logging.info("Thread %s: finishing", ip)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    threads = list()
    ip = ['10.245.46.207', '10.245.46.208']
    for index in ip:
        logging.info("Main    : create and start thread %s.", index)
        x = threading.Thread(target=main, args=(index,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %s.", index)
        thread.join()
        logging.info("Main    : thread %s done", index)
