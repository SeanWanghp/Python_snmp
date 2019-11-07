# coding=utf-8                                                                  #this must be in first line
#C:\Python27\Doc python
__author__='Sean Wang'
#data@:2019-02-19
#update data@:2019-xx-xx
# coding=gbk                                                                    #spell inspection cancelled
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word
import socket
import subprocess
import multiprocessing
import logging
from basic_lib.SNMP_basic_lib.pysnmp_pool import main
from time import sleep
from contextlib import contextmanager
'''
sk.bind(address)
　　s.bind(address) 将套接字绑定到地址。address地址的格式取决于地址族。在AF_INET下，以元组（host,port）的形式表示地址。

sk.listen(backlog)
　　开始TCP监听。backlog指定在拒绝连接之前，操作系统可以挂起的最大连接数量。该值至少为1，大部分应用程序设为5就可以了.
    backlog等于5，表示内核已经接到了连接请求，但服务器还没有调用accept进行处理的连接个数最大为5
    这个值不能无限大，因为要在内核中维护连接队列

sk.setblocking(bool)
　　是否阻塞（默认True），如果设置False，那么accept和recv时一旦无数据，则报错。

sk.accept()
　　接受连接并返回（conn,address）,其中conn是新的套接字对象，可以用来接收和发送数据。address是连接客户端的地址。
　　接收TCP 客户的连接（阻塞式）等待连接的到来

sk.connect(address)
　　连接到address处的套接字。一般，address的格式为元组（hostname,port）,如果连接出错，返回socket.error错误。

sk.connect_ex(address)
　　同上，只不过会有返回值，连接成功时返回 0 ，连接失败时候返回编码，例如：10061

sk.close()
　　关闭套接字

sk.recv(bufsize[,flag])
　　接收TCP数据，数据以字符串形式返回，bufsize指定要接收的最大数据量。flag提供有关消息的其他信息，通常可以忽略。

sk.recvfrom(bufsize[.flag])
　　接收UDP数据，与recv()类似, 但返回值是（data,address）.其中data是包含接收数据的字符串,address是发送数据的套接字地址.

sk.send(string[,flag])
　　#发送TCP数据，将string中的数据发送到连接的套接字。返回值是要发送的字节数量，该数量可能小于string的字节大小。
　　#Python 3必须转换为字节形式bytes发送

sk.sendall(string[,flag])
　　#完整发送TCP数据，完整发送TCP数据。将string中的数据发送到连接的套接字，但在返回之前会尝试发送所有数据。
    成功返回None，失败则抛出异常
　　#Python 3必须转换为字节形式bytes发送
    内部通过递归调用send，将所有内容发送出去。

sk.sendto(string[,flag],address)
　　将数据发送到套接字，address是形式为（ipaddr，port）的元组，指定远程地址。返回值是发送的字节数。该函数主要用于UDP协议。

sk.settimeout(timeout)
　　设置套接字操作的超时期，timeout是一个浮点数，单位是秒。值为None表示没有超时期。一般，超时期应该在刚创建套接字时设置，因为它们可能用于连接的操作（如 client 连接最多等待5s ）

sk.getpeername()
　　返回连接套接字的远程地址。返回值通常是元组（ipaddr,port）。

sk.getsockname()
　　返回套接字自己的地址。通常是一个元组(ipaddr,port)

sk.fileno()
　　套接字的文件描述符
'''


class socket_process(object):
    def __init__(self):
        pass

    def run_snmp(self, times):
        """
        Get snmp walking log.
        :Args:
         - None

        :Returns:
         - snmp walking - the element if it was found

        :Raises:
         - NoRespond from EQPT

        :Usage:
            pysnmp.nextcmd, getcmd, bulkcmd
        """
        return self._snmp_run(times)

    def cmd_run(self):
        """
        Finds an element by a partial match of its link text.
        :Args:
         - None

        :Returns:
         - cmd log

        :Raises:
         - NoSuchElementException - if the element wasn't found

        :Usage:
            telnet or ping .......
        """
        return self._run_cmd()

    def _snmp_run(self, times):
        '''C:\\Python27\\Doc\\basic_lib\\SNMP_basic_lib\\pysnmp_lib_main.py'''
        ip = '10.245.46.207'
        port = '161'
        msg = ['10.245.46.208', ip]
        tel_port = ['161', port]
        main(msg, tel_port, times)

    def _run_cmd(self):
        cmd = "cmd.exe"
        begin = 1
        end = 3
        while begin < end:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                 stdin=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            p.stdin.write(b"ping 192.168.37." + str(begin).encode('ascii') + b"\n")
            p.stdin.write(b"tracert 192.168.37." + str(begin).encode('ascii') + b"\n")
            p.stdin.close()
            p.wait()
            begin = begin + 1
            print(begin)
            print("execution result: %s" % p.stdout.read().decode('utf-8'))
        else:
            print('**********************The while loop is over.******************************')


class Fileopen(object):
    @contextmanager
    def file_open(self, path):
        f_obj = None
        try:
            f_obj = open(path, mode="w")
            yield f_obj
        except OSError:
            print("We had an error!")
        finally:
            print("Closing file")
            f_obj.close()


class socket_cla(socket_process):
    def __init__(self):
        '''SOCKET是(源IP+源PORT+目的IP+目的PORT), socket(ip, port) as telnet(ip, port) are different pipe
        参数一：地址簇
    　　socket.AF_INET IPv4（默认）
    　　socket.AF_INET6 IPv6
    　　socket.AF_UNIX 只能够用于单一的Unix系统进程间通信
        参数二：类型
    　　socket.SOCK_STREAM　　流式socket , for TCP （默认）
    　　socket.SOCK_DGRAM　　 数据报式socket , for UDP
    　　socket.SOCK_RAW 原始套接字，普通的套接字无法处理ICMP、IGMP等网络报文，而SOCK_RAW可以；其次，
        SOCK_RAW也可以处理特殊的IPv4报文；此外，利用原始套接字，可以通过IP_HDRINCL套接字选项由用户构造IP头。
    　　socket.SOCK_RDM 是一种可靠的UDP形式，即保证交付数据报但不保证顺序。SOCK_RAM用来提供对原始协议的低级访问，
        在需要执行某些特殊操作时使用，如发送ICMP报文。SOCK_RAM通常仅限于高级用户或管理员运行的程序使用。
    　　socket.SOCK_SEQPACKET 可靠的连续数据包服务
        参数三：协议
    　　0　　（默认）与特定的地址家族相关的协议,如果是 0 ，则系统就会根据地址格式和套接类别,自动选择一个合适的协议
        '''
        super(socket_cla, self).__init__()
        hostname = socket.gethostname()
        print("Host name: %s" % hostname)
        sysinfo = socket.gethostbyname_ex(hostname)
        ip_addr = sysinfo[2]
        ip_addr1 = ip_addr[0]
        logging.warning("IP Address: %s" % ip_addr1)
        self.ip_port = (ip_addr1, 8888)

    def skpk(self):
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_RAW)  # recv RAW packet
        self.sk.bind(self.ip_port)

    def tcpsk(self):
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)  # recv TCP packet
        self.sk.bind(self.ip_port)
        '''the following command using for TCP connection, listen() and accept() for TCP'''
        self.sk.listen(5)
        self.conn, self.addr = self.sk.accept()
        logging.warning(self.addr)
        # self.sk.connect(('10.245.46.208', 23))    #this is server side, can not use connect(client) function
        self.data = self.conn.recv(1024)     #TCP
        self.conn.send(b'I have been already get the message!')

    def udpsk(self):
        # ip_port = ('10.245.46.201', 23)
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)   #recv UDP packet
        self.sk.bind(self.ip_port)
        self.data = self.sk.recvfrom(4096)  # UDP

    def skdns(self):
        '''checkout the DNS of the web'''
        host = "www.163.com"
        DNS_IP = socket.getaddrinfo(host, None)
        print("DNS IP is: ", DNS_IP[0][4][0])

    def socket_run(self):
        '''send(), sendall() and recv() for TCP, sendto() and recvfrom() for UDP'''
        while True:
            # self.skpk()
            self.tcpsk()
            # self.udpsk()
            print('sk.getpeername(): {}'.format(self.sk.getsockname()))
            with Fileopen().file_open("udp_packet_cap.txt") as fobj:
                fobj.seek(0)
                fobj.truncate()  # 清空文件
                for dd in str(self.data).split(','):
                    # print('get data from udp client: {}\r'.format(dd))
                    for msg in dd.split('\n'):
                        print("msg: ", msg.encode("utf-8"))
                        if 'ping' in msg:
                            print('enter ping')
                            self.cmd_run()
                        elif 'snmp' in msg:
                            print('enter snmp')
                            self.run_snmp('2')
                        else: pass
                        fobj.write(str(dd) + '\n')


if __name__ == "__main__":
    soc = socket_cla()
    soc.socket_run()
    '''https://www.jianshu.com/p/629961795744 介绍说明'''

#####SOCKET CLIENT as following
# ip_port = ('localhost', 8080)
# sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
# while True:
#     inp = raw_input('data: ').strip()
#     if inp == 'exit':
#         break
#     sk.sendto(inp, ip_port)
