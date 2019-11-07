#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：server.py

# import socket               # 导入 socket 模块
# s = socket.socket()         # 创建 socket 对象
# host = socket.gethostname() # 获取本地主机名
# port = 12345                # 设置端口
# s.bind((host, port))        # 绑定端口
# s.listen(5)                 # 等待客户端连接
# while True:
#     c, addr = s.accept()     # 建立客户端连接。
#     print '连接地址：', addr
#     c.send('欢迎访问菜鸟教程！')
#     # c.close()                # 关闭连接

# 创建SocketServerTCP服务器：
import SocketServer
from SocketServer import StreamRequestHandler as SRH
from time import ctime

host = "localhost"
port = 9999
addr = (host, port)


class Servers(SRH):
    def handle(self):
        print 'got connection from ', self.client_address
        self.wfile.write('connection %s:%s at %s succeed!' % (host, port, ctime()))
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            print "Recv from %s word: %s"%(self.client_address[0], data)
            data = raw_input("Please reply you word:>")
            self.request.sendall(data)
            # print "Recv from %s word: %s" % (self.client_address[0], data)

print 'server is running....'
server = SocketServer.ThreadingTCPServer(addr, Servers)
server.serve_forever()