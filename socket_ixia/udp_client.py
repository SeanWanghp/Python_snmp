# coding=utf-8                                                                  #this must be in first line
#C:\Python27\Doc python
__author__='Sean Wang'
#data@:2018-08-17
# coding=gbk                                                                    #spell inspection cancelled
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word
#SOCKET    https://www.cnblogs.com/aylin/p/5572104.html

import sys, socket
####SOCKET CLIENT as following
hostname = socket.gethostname()
print ("Host name: %s" % hostname)
sysinfo = socket.gethostbyname_ex(hostname)
ip_addr = sysinfo[2]
ip_addr1 = ip_addr[0]
print("IP Address: %s" % ip_addr1)
ip_port = (ip_addr1, 8080)
sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
while True:
    inp = raw_input('data(ping, snmp): ').strip()
    '''inp effect value: ping, snmp'''
    if inp == 'exit':
        break
    sk.sendto(inp, ip_port)
    # print 'sk.getpeername(): {}'.format(sk.getpeername())