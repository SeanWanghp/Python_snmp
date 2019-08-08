# coding=utf-8                                                                  #this must be in first line
#C:\Python27\Doc python
__author__='Sean Wang'
#data@:2019-08-08
#update data@:2019-08-08
# coding=gbk                                                                    #spell inspection cancelled
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word
import socket                   # Import socket module
from time import sleep


def login_print(s, command):
    s.send((command + '\n').encode())   #exchange the code mode
    sleep(1)    #wait until recv all message
    data = s.recv(4096)
    print "run:", data
    return data


def send_recv_print(s, command):
    login_print(s, 'e7support')
    res = login_print(s, 'admin')   #will showing up unknow code, only input and ignore it
    if b'>' in res:
        for com in command:
            login_print(s, com)


s = socket.socket()             # Create a socket object
tel = s.connect(('10.245.46.215', 23))
s.settimeout(5)
global data
print('receiving init...')
login_print(s, '\n')

command = ['set se pa di', 'show vlan', 'show card', 'show session', 'show mcast', 'show dhcp lease']
send_recv_print(s, command)

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