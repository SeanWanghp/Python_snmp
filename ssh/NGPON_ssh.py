# --encoding=UTF-8--
# coding=gbk
__author__ = 'Maojun Wang'
import multiprocessing
import telnetlib
import paramiko
import subprocess
import string
import os
import sys
import logging
import datetime
from time import sleep
import re as sre
from multiprocessing import Process
from E7.SLV384.deco_slv import log_pa, slv_log
from config_yaml_lib import yaml_parameter, telnet_parameters
"""source code:      
https://www.shiyanlou.com/courses/?course_type=all&tag=Python&fee=all&page=7
http://blog.csdn.net/oatnehc/article/details/46580753
http://www.361way.com/python-paramiko-ssh/3984.html
"""


cli_steps = """terminal screen-length 0
            #paginate false
            #cli show default disable
            idle-timeout 0
            session notification set-category all
            # cli telnet enable
            # cofiguration running as following command
            show file contents syslog
            # show running-config
            show run vlan
            show run policy-map
            show run class-map
            show run ntp
            show clock
            show run snmp
            show inter la la1 mem
            show inter la la1 counters
            show inter sum
            show interface pon 1/1/xp1 status
            show interface ethernet 1/1/x2 counters interface-counters tx-pkts
            show inter craft 1
            config
            inter la la1
            end
            show inter craft 2
            #show inter eth
            #show inter line
            show inter sum
            #reload
            """


class Attr:
    def __getattr__(self, value):  # This is equal to self.value, it'll do all not provisioned parameters checking
        if value == 'prompt':
            return '# '
        elif value == 'reload':
            return 'y/N '
        elif value == 'recv':
            return 9999
        elif value == 'buff_cli':
            return ''
        elif value == 'enter':
            return '\n'     # LINUX system just need \n is fine

    def __setattr__(self, attrname, value):
        """This is equal to self.attrname = value, it'll do all (try to provisioned) parameters checking"""
        if attrname in self.private:
            print('attrname is in self.name')
        else:
            self.__dict__[attrname] = value


class Milanlib(Attr, yaml_parameter):
    private = ['name']

    def __init__(self):
        """paramiko模块是基于Python实现的SSH远程安全连接，用于SSH远程执行命令、文件传输等功能。
        默认Python没有，需要手动安装：pip install paramiko
        如安装失败，可以尝试yum安装：yum install python-paramiko
        """
        self.enter = '/r'
        self.buff_cli = ''
        pass

    def __del__(self):
        """说明：__del__方法是在程序(class)退出时调用的"""
        print("milan_lib running finished!")

    def linux_mode(self, client, cli_steps):
        if isinstance(cli_steps, list):
            for cli in cli_steps:
                stdin, stdout, stderr = client.exec_command(cli.encode('ascii'), get_pty='# ')
                print(stdout.readlines())
                for std in stdout.readlines():
                    print("read content:", std)
        elif isinstance(cli_steps, str):
            for cli in cli_steps.split('\n'):
                print(cli)
                stdin, stdout, stderr = client.exec_command(cli.encode('ascii'), get_pty='# ')
                print("readlines:", stdout.readlines())
                # for std in stdout.readlines():
                #     print("read content:", std.decode('utf-8'))
        # if client in self:       #magic method, do not using it in running
        #     print("passsssssssssssssssssss"

    @slv_log(author='ROOT')  # Decorator will print(the result
    def axos_command(self, ssh_session, cli_steps):
        print(self.name, self.grade)
        print(type(cli_steps))
        try:
            if isinstance(cli_steps, list):
                for cli in cli_steps:
                    ssh_session.exec_command(cli + self.enter)
                    buff = ''
                    while not buff.endswith(self.prompt):
                        print(buff, '111111111111111111111111111111111')
                        resp = ssh_session.recv(self.recv)
                        buff += resp
                    self.buff_cli += buff

            elif isinstance(cli_steps, str):

                for cli in cli_steps.splitlines():
                    print('cli: ', cli)
                    stdin, stdout, stderr = ssh_session.exec_command(cli.encode('ascii'))
                    print('stdout: ', stdout.read().decode(encoding='utf-8'))
                    # while not buff.endswith('# '):
                    #     print(buff, '22222222222222222222222222222222222222')
                    #     # resp = ssh_session.recv(self.prompt or self.reload)
                    #     resp = ssh_session.recv(9999)
                    #     print(resp)
                    #     buff += resp
                    # self.buff_cli += buff.strip()
            # print("buff_cli:", self.buff_cli)

        except Exception:
                print(Exception)
        return self.buff_cli


# @log_pa("SSH to NGPON")
def func(*args):
    ip, port = args
    tn = Milanlib()
    # super(milan_lib, self).__setattr__('prompt', '# ')
    tn.name = 'seanwang'
    tn.grade = 11
    # getattr(tn, 'recv', setattr(tn, 'recv', 9999))
    # getattr(tn, 'prompt', setattr(tn, 'prompt', '# '))
    # print(tn.prompt
    print("SSH ip is: %s, port is: %s" % (ip, port))

    try:
        paramiko.util.log_to_file('test.txt')
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port, username='root', password='root', timeout=4)
        #Linux mode with command running
        steps = '''pwd
                    pwd'''
        tn.linux_mode(client, steps)

        #CLI command switch running
        # ssh = client.invoke_shell()
        buff = ''
        # while not buff.endswith('~# '):
        #     resp = ssh.recv(9999)
        #     buff += resp
        #     print("buff start:", buff.upper())

        sys_steps = """show file contents syslog
                    show running-config
                    """
        client.connect(ip, port, username='sysadmin', password='seanwang', timeout=4)
        for i in range(0, 1):
            print(f'times: {i}')
            tn.axos_command(client, cli_steps)
        return buff

    except IOError:
        tel_error = sre.compile(r"((error)|(time))")
        if tel_error.search(str(ex)):
            print('*' * 100)
            print('*' * 100)
    return ssh


if __name__ == '__main__':
    '''MILAN change card mode with threading on different shelves'''
    for i in range(1, 2):
        yaml_pa = yaml_parameter()
        milan_dict = {'10.245.37.204': 22,
                      yaml_pa.axos_ngpon2x4_1_host: yaml_pa.axos_ngpon2x4_1_port,
                      '10.245.88.150': 22,
                      '10.245.46.207': 22}
        print("yaml_parameter:", yaml_pa.__dict__)
        print(yaml_pa.axos_ngpon2x4_2_host)
        print(yaml_pa.axos_ngpon2x4_2_port)
        milan_dict = {yaml_pa.axos_ngpon2x4_2_host: yaml_pa.axos_ngpon2x4_2_port,}
        # milan_dict = {yaml_pa.axos_35b_1_host: yaml_pa.axos_35b_2_port, yaml_pa.axos_35b_2_host: yaml_pa.axos_35b_2_port, }
        pool = multiprocessing.Pool(processes=len(milan_dict))
        print(milan_dict)
        print(milan_dict.keys())
        # for (ip, port) in zip(msg, ssh_port):             #this is for loop parameters, but using little
        for ip, port in milan_dict.items():  # iteritor 字典迭代器
            pool.apply_async(func, args=(ip, port))  # thread running two E7 process
        pool.close()
        pool.join()
        print("Multiprocessing(es) done!")
