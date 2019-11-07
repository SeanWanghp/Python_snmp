#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：client.py

# import socket               # 导入 socket 模块
# s = socket.socket()         # 创建 socket 对象
# host = socket.gethostname() # 获取本地主机名
# port = 12345                # 设置端口好
# s.connect((host, port))
# print s.recv(1024)
# # s.close()


from socket import *

host = "localhost"
port = 9999
bufsize = 1024
addr = (host, port)
client = socket(AF_INET, SOCK_STREAM)
client.connect(addr)
while True:
    data = raw_input("Please enter you word:>")
    if not data or data == 'exit':
        break
    client.sendall('%s\r\n' % data)
    data = client.recv(bufsize)
    if not data:
        break
    print(data.strip())
client.close()