# coding=utf-8                                                                  #this must be in first line
#C:\Python27\Doc python
__author__='Sean Wang'
#data@:2018-08-17
# coding=gbk                                                                    #spell inspection cancelled
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word
#SOCKET    https://www.cnblogs.com/aylin/p/5572104.html

import sys, socket, logging
####SOCKET CLIENT as following
hostname = socket.gethostname()
print ("Host name: %s" % hostname)
sysinfo = socket.gethostbyname_ex(hostname)
ip_addr = sysinfo[2]
ip_addr1 = ip_addr[0]
print("IP Address: %s" % ip_addr1)
ip_port = (ip_addr1, 8888)
sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
while True:
    inp = input('data(ping, snmp): ').strip()
    '''inp effect value: ping, snmp'''
    if inp == 'exit':
        break
    if inp == 'snmp':
        sk.sendto(inp.encode('ascii'), ip_port)
        print('snmp running in udp server, please check it by manual')
    elif inp == 'ping':
        sk.sendto(inp.encode('ascii'), ip_port)
        logging.warning('ping running in udp server, please check it by manual')
    # print 'sk.getpeername(): {}'.format(sk.getpeername())