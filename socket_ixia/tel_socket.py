# coding=utf-8                                                                  #this must be in first line
# C:\Python27\Doc python
__author__ = 'Sean Wang'
#data@:2019-08-08
#update data@:2019-08-08
"""print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word"""
import socket
import sys
import os
import logging
import threading
import time
from time import sleep


class Celsius:
    """property sample"""
    def __init__(self, temperature=0):
        self.temperature = temperature

    def to_fahrenheit(self):
        return (self.temperature * 1.8) + 32

    def get_temperature(self):
        return self._temperature

    def set_temperature(self, value):
        if value != 23:
            logging.warning(ValueError("Temperature below -273 is not acceptable"))
        elif value == 23:
            logging.warning("telnet port value is 23")
            self._temperature = value
        else:
            raise Exception(t + 'an error generated')

    temperature = property(get_temperature, set_temperature)


def login(host, port):
    """This is socket client for socket.socket
    socket.connect is for client connect to server port
    """
    ss = socket.socket()
    ss.settimeout(5)
    ss.connect((host, port))
    return ss


def log(ip, port):
    def decorator(func):
        def wrapper(*args, **kw):
            login(ip, port)
            return func(*args, **kw)
        return wrapper
    return decorator


# @log('10.245.46.215', 23)
def login_print(ss, command):
    """sleep for wait recv messages, encode for exhcange code"""
    global data
    ss.send((command.encode('ascii') + b'\n'))
    sleep(0.5)
    data = ss.recv(4096)
    if command is '\n':
        print(data)
    else:
        print(data.decode('utf_8'))
    return data


def send_recv_print(s, command):
    login_print(s, 'e7support')
    """will get unknow code with following login, no way to avoid it till now"""
    res = login_print(s, 'admin')
    if b'>' in res:
        for com in command:
            login_print(s, com)


def main(ip):
    cc = Celsius()
    cc.temperature = 23
    port = cc.temperature
    ss = login(ip, port)
    login_print(ss, '\n')
    command = [
        'set sess pa di ti di',
        'show vlan',
        'show card',
        ]
    send_recv_print(ss, command)
    ss.close()
    logging.info('python version: {}'.format(sys.version))
    snmp_oid = '.1.3.6.1.2.1.1'
    """snmp running in python37 easy way"""
    out = os.popen('python c:\\Python37\\Scripts\\snmpbulkwalk.py -v 2c -c public 10.245.46.208 {}'.format(snmp_oid))
    for sn in (out.read().encode('utf-8').splitlines()):
        print(sn)


class Test(threading.Thread):
    def __init__(self, num, ip):
        threading.Thread.__init__(self)
        self._num = num
        self.count = 1
        self.mutex = threading.Lock()
        self.ip = ip

    def run(self):
        self.mutex.acquire()
        threadname = threading.currentThread().getName()
        for times in range(0, int(self._num)):
            count = self.count + 1
            print(threadname, times, count)
            main(ip)
        self.mutex.release()

    def __del__(self):
        if th.is_alive():
            print('still running')
        else:
            logging.warning('threading finished')


if __name__ == '__main__':
    threads = []
    th = None
    th_num = 3
    run_num = 1
    ip = '10.245.46.215'
    """append for create thread
    join for thread run at same time
    """
    for x in range(0, th_num):
        threads.append(Test(run_num, ip, ))
    for th in threads:
        th.start()
    """this will run at same time, run one by one need put join into the FOR"""
    for index, thread in enumerate(threads):
        logging.warning("Main    : before joining thread %d.", index)
        thread.join()
        logging.warning("Main    : thread %d done", index)



####https://blog.csdn.net/qq_43017750/article/details/89133829
# class Telnet(object):
#     def __init__(self, ):
#         self.remote_addr = '10.245.46'
#         self.remote_port = 23
#         self.username = "e7support"
#         self.password = "admin"
#         self.timeout = 5
#         self.login_timeout = 1
#         self.send_cmd_timeout = 0.5
#         self.system_name = ""
#         self.buffer = 4096
#         self.file_name = self.remote_addr + ".log"
#         self.client = None
#
#     def Initialization_continue(self):
#         self.client = socket.socket()
#         self.client.connect((self.remote_addr, self.remote_port))
#         self.client.settimeout(self.timeout)
#
#     def Initialization_file(self):
#         self.file_name = (self.system_name + self.remote_addr + ".log").replace("\r\n#\r\n" ,"")
#         print (self.file_name)
#         with open(self.file_name, "w") as save_object:
#             save_object.write("")
#
#     def login(self,):
#         tag = 0
#         while True:
#             if not (tag == 1):
#                 self.client.send("\n".encode())
#                 time.sleep(self.login_timeout)
#             data = self.client.recv(self.buffer)
#             if b"Username" in data:
#                 print (data)
#             else:
#                 print ("没有找到用户名")
#                 tag = 1
#                 continue
#             self.client.send((self.username + "\n").encode())
#             print ("发送: " +(self.username + "\n"))
#             time.sleep(self.login_timeout)
#             data = self.client.recv(self.buffer)
#             if b"Password" in data:
#                 print (data)
#             else:
#                 print ("没有找到密码")
#                 tag = 1
#                 continue
#             self.client.send((self.password +"\n").encode())
#             print ("发送: " +(self.password +"\n"))
#             time.sleep(self.login_timeout)
#             data = self.client.recv(self.buffer)
#             if b">" in data:
#                 print ("登陆成功")
#                 break
#             else:
#                 print ("登陆失败，正在重新登陆")
#                 tag = 1
#                 continue
#
#     def send_cmd(self, cmd):
#         self.client.send(("    " + cmd + "\n").encode())
#         print ("发送命令: " +("    " + cmd + "\n"))# 发送命令
#         time.sleep(self.send_cmd_timeout)
#         data = self.client.recv(self.buffer)
#         tag = self.recv(data)
#         print (tag)
#         while True:
#             if tag == 0:
#                 self.client.send("    \n".encode())
#                 print ("发送空格")
#                 time.sleep(self.send_cmd_timeout)
#                 data = self.client.recv(self.buffer)
#                 tag = self.recv(data)
#             else:
#                 break
#
#     def recv(self, data):
#         if b"---- More ----" in data:
#             self.output(data)
#             return 0
#         else:
#             self.output(data)
#             return 1
#         if not((b">" in data) or (b"[" in data)):
#             self.output(data)
#             return 0
#
#     def output(self, data):
#         msg = data.decode().replace("[16D                [16D", "").replace("  ---- More ----", "")
#         if "sysname" in msg.split(" "):
#             number = msg.split(" ").index("sysname")
#             self.system_name = msg.split(" ")[number +1]
#             self.Initialization_file()
#         print (msg)
#         with open(self.file_name, "a") as save_object:
#             save_object.write(msg)
#
#
# ips = ["10.245.46.215"]
# for ip in ips:
#     telnet = Telnet()
#     telnet.remote_addr = ip
#     telnet.Initialization_continue()
#     telnet.login()
#     command = ['show vlan', 'show card', 'show session', 'show mcast', 'show dhcp lease']
#     for com in command:
#         telnet.send_cmd(com)