# coding=utf-8                                                                  #this must be in first line
#C:\Python27\Doc python
__author__='Sean Wang'
#data@:2018-08-17
# coding=gbk                                                                    #spell inspection cancelled
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word


#SOCKET    https://www.cnblogs.com/aylin/p/5572104.html

import sys, socket
# package

from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()
driver.get("https://www.baidu.com/")

driver.find_element("id", "kw").send_keys("yoyoketang")
driver.find_element('css selector', "#su").click()
driver.close()


host = "www.163.com"

DNS_IP = socket.getaddrinfo(host, None)
print socket.create_connection(('10.245.46.205', 23))

print DNS_IP
print "DNS IP is: ", DNS_IP[0][4][0]

import socket
import select


sk1 = socket.socket()
sk1.bind(("127.0.0.1", 8001))
sk1.listen(2)

sk2 = socket.socket()
sk2.bind(("127.0.0.1", 8002))
sk2.listen(2)

sk3 = socket.socket()
sk3.bind(("127.0.0.1", 8003))
sk3.listen(2)

li = [sk1, sk2, sk3]

while True:
    r_list, w_list, e_list = select.select(li, [], [], 1) # r_list可变化的
    for line in r_list:
        conn, address = line.accept()
        conn.sendall(bytes("Hello World !",encoding="utf-8"))