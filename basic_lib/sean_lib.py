#-*- coding: UTF-8 -*-

#使用socket模块
import socket
#得到本地ip
localIP = socket.gethostbyname(socket.gethostname())
print("local ip:%s "%localIP)

ipList = socket.gethostbyname_ex(socket.gethostname())
for i in ipList:
    if i != localIP:
       print("external IP:%s"%i)


import struct
ip = '192.168.1.1'
num_ip=socket.ntohl(struct.unpack("I", socket.inet_aton(str(ip)))[0])
print(num_ip)
ip = socket.inet_ntoa(struct.pack('I', socket.htonl(num_ip)))
print(ip)


import ipaddress
print("ipv4address:", ipaddress.IPv4Address("0000"))

def valid_ip(address):
    try:
        socket.inet_aton(address)
        return True
    except:
        return False

print(valid_ip('0.0.0.1'))
print(valid_ip('225.10.20.30'))
print(valid_ip('gibberish'))


import yaml
stream = file('topo.yaml', 'r')
dict = yaml.load(stream)   #ymal.dump(data, stream) 用来写入数据
# print dict
#打印所有的yaml数据，其实也就是dict类，《简明_python_教程》里说的字典
for data, value in dict.items():
    # print data, value
    for data_1, value_1 in value.items():
        # print data, data_1, value_1
        for data_2, value_2 in value_1.items():
            print(data, data_1, data_2, value_2)
print(dict["E7"]['n1']['host'], dict["E7"]['n1']['port'])
print(dict["E7"]['n1']['username'], dict["E7"]['n1']['password'])
stream.close()


class telnet_parameters(object):
    '''
    property method: set and get value, set value can be using for check value
    '''
    def __init__(self, port=23, timeout=100):
        self.__port     = port
        self.__timeout  = timeout
        self.__host     = '127.0.0.1'

    @property
    def host(self):
        return self.__host, self.__port

    @host.setter
    def host(self, value):
        '''
        set up host value
        '''
        ip_host = socket.ntohl(struct.unpack("I", socket.inet_aton(str(value)))[0])
        if not isinstance( ip_host, long):
            raise ValueError('__host must be an long!')
        if ip_host > 4294967294 or ip_host < 0:
            raise ValueError('__host must between 0 ~ 4294967295!')
        self.__host = value


telnet_pa = telnet_parameters(None, None)
telnet_pa.host = '10.245.47.231'
print("telnet_pa.host:", telnet_pa.host)