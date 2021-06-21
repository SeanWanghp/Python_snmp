# coding=utf-8
# Date ：2020/9/8 9:51
# Modify Date ：2020/10/27
__author__ = 'Maojun'

import time
import threading
import struct
import sys
import socket
import logging
import logging.handlers
import platform
import re

if sys.version_info < (3, 0):
    print("please upgrade python to 3.0")
else:
    pass

pc_mac = '989096c18631'
ciscoinc_3b = '04|c5|a4|3b|e7|f0'
debug = False

"""先要从E7抓取正常的IPDR交互报文，再从E7导出，用WIRESHARK另存为TXT，再把16进制数据取出来，如下是原始数据
协议文档里暂时没找到交互报文的原始数据，只能从系统交互中取原始数据暂时"""

ipdr_tcp_original_data = ['|00|02|5d|fd|a2|e5|04|c5|a4|3b|e7|f0|08|00|45|00|00|3c|7a|a8|40|00|3f|06|81|2e|0a|f5|fb|21'
                          '|0a|f5|2e|da|9e|44|12|81|52|21|d4|fd|00|00|00|00|a0|02|39|08|9d|68|00|00|02|04|05|b4|04|02'
                          '|08|0a|ab|6f|ae|55|00|00|00|00|01|03|03|07|']
ipdr_tcp_data = ['|00|02|5d|fd|a2|e5|04|c5|a4|3b|e7|f0|08|00|45|00|00|3c|7a|a8|40|00|3f|06|81|2e|c0|a8|25|c5'
                 '|0a|f5|2e|da|9e|44|12|81|52|21|d4|fd|00|00|00|00|a0|02|39|08|9d|68|00|00|02|04|05|b4|04|02'
                 '|08|0a|ab|6f|ae|55|00|00|00|00|01|03|03|07|']
ipdr_conn_original_data = ['|00|02|5d|fd|a2|e5|98|90|96|c1|86|31|08|00|45|00|00|67|7a|aa|40|00|3f|06|81|01|'
                           '0a|f5|fb|21|0a|f5|2e|da|9e|44|12|81|52|21|d4|fe|76|e6|df|19|80|18|00|73|3c|76|00|00'
                           '|01|01|08|0a|ab|6f|ae|61|cc|09|b7|46|02|05|00|00|00|00|00|33|0a|f5|fb|21|12|82|00|00|00'
                           '|02|00|00|00|14|00|00|00|19|41|63|74|69|76|65|20|42|72|6f|61|64|62|61|6e|64|20|4e|65|74'
                           '|77|6f|72|6b|73|']

ipdr_connection_data = ['|02|05|00|00|00|00|00|33|c0|a8|25|c5|12|82|00|00|00|02|00|00|00|14|'
                        '00|00|00|19|41|63|74|69|76|65|20|42|72|6f|61|64|62|61|6e|64|20|4e|65|74|77|6f|72|6b|73']
ipdr_session_data = ['|02|14|00|00|00|00|00|0a|00|01']
ipdr_gettemp_data = ['|02|16|01|00|00|00|00|0a|00|02']
ipdr_flowstart_data = ['|02|01|01|00|00|00|00|08']
ipdr_finalack_data = ['|02|13|01|00|00|00|00|08']
ipdr_keeplive_data = ['|02|40|00|00|00|00|00|08']

pc_tcp_conn = ipdr_tcp_data[0].replace('|', '')
pc_ipdr_connection = ipdr_connection_data[0].replace('|', '\\x')
pc_ipdr_session = ipdr_session_data[0].replace('|', '\\x')
pc_ipdr_gettemp = ipdr_gettemp_data[0].replace('|', '\\x')
pc_ipdr_flowstart = ipdr_flowstart_data[0].replace('|', '\\x')
pc_ipdr_finalack = ipdr_finalack_data[0].replace('|', '\\x')
pc_ipdr_keeplive = ipdr_keeplive_data[0].replace('|', '\\x')

print(pc_ipdr_connection)
print(pc_ipdr_session)
print(pc_ipdr_gettemp)
print(pc_ipdr_flowstart)
print(pc_ipdr_finalack)
print(pc_ipdr_keeplive)

if debug:
    time.sleep(300)


def long2ip(long):
    """transfer int to ipv4"""
    floor_list = []
    yushu = long
    for i in reversed(range(4)):  # 3,2,1,0
        res = divmod(yushu, 256 ** i)
        floor_list.append(str(res[0]))
        yushu = res[1]
    return '.'.join(floor_list)


def gettime(seconds, aa):
    timearray = time.localtime(seconds)
    otherstyletime = time.strftime("%H:%M:%S", timearray)
    print("{}: {}".format(aa, otherstyletime))


def subZero(ipseg):
    index = 0
    for i in range(len(ipseg)):
        if ipseg[i] == '0':
            index += 1
        else:
            break
    if index >= 2:
        return ipseg[index:] if ipseg[index:] else '0'
    else:
        return ipseg


def dec2ipv6(dec):
    """transfer dec to ipv6"""
    if checkdec(dec) and int(dec) <= 340282366920938463463374607431768211455:
        hexstr = (hex(int(dec)))[2:]
        hexstrlen = len(hexstr)
        while hexstrlen < 32:
            hexstr = '0' + hexstr
            hexstrlen += 1
            result = subZero(hexstr[0:4]) + ":" + subZero(
                hexstr[4:8]) + ":" + subZero(
                hexstr[8:12]) + ":" + subZero(hexstr[12:16]) + ":" + subZero(
                hexstr[16:20]) + ":" + subZero(hexstr[20:24]) + ":" + subZero(
                hexstr[24:28]) + ":" + subZero(hexstr[28:])
            print("ipv6address:" + result)
            return result
    else:
        return ""


def checkdec(dec):
    matchobj = re.match(r'(0[dD])?[0-9]+$', dec)
    if matchobj:
        return True
    else:
        return False


class Ipdrrun:
    def __init__(self, netflow_sock, ipdr_port, axos_ip, localip, localport):
        self.netflow = netflow_sock
        self.port = ipdr_port
        self.axos_ip = axos_ip
        self.localport = localport
        self.localip = localip
        self.ipdrmain()

    def ipdrmain(self):
        while True:
            print("self.axos_ip: ", self.axos_ip, self.port)

            if platform.system() == 'Windows':
                self.netflow.connect((self.axos_ip, self.port))  # TCP connection set up
            elif platform.system() == 'Linux':
                """netstat -anp |grep 4737      check port status
                    fuser -v -n tcp 4737    check port process ID"""
                self.netflow.connect((axos_ip, ipdr_port))
            logging.warning("Connection to port {} : {}".format(self.axos_ip, self.port))

            while self.netflow:
                time.sleep(3)
                print('sending', pc_ipdr_connection)
                """all IPDR data capture by wireshark"""

                ipdr_session_up = [
                    b'\x02\x05\x00\x00\x00\x00\x00\x33\xc0\xa8\x25\xc5\x12\x82\x00\x00\x00\x02\x00\x00\x00'
                    b'\x14\x00\x00\x00\x19\x41\x63\x74\x69\x76\x65\x20\x42\x72\x6f\x61\x64\x62\x61\x6e\x64'
                    b'\x20\x4e\x65\x74\x77\x6f\x72\x6b\x73',
                    b'\x02\x14\x00\x00\x00\x00\x00\x0a\x00\x01',
                    b'\x02\x16\x01\x00\x00\x00\x00\x0a\x00\x02'
                    b'\x02\x01\x01\x00\x00\x00\x00\x08',
                    b'\x02\x13\x01\x00\x00\x00\x00\x08']

                ipdr_keep_data = [b'\x02\x40\x00\x00\x00\x00\x00\x08']
                ipdr_data_ack = [b'\x02\x21\x01\x00\x00\x00\x00\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01']

                value_all = []
                all_para = []
                message_id = 0

                for data in ipdr_session_up:
                    "only need send protocol part after TCP connection set up"
                    self.netflow.send(data)
                    ipdr_conn_data = self.netflow.recv(1024)
                    print('ipdr_conn_data:', ipdr_conn_data)

                    if len(ipdr_conn_data) is 0:
                        pass
                    else:
                        # Unpack the packet head
                        (version,) = struct.unpack('!B', ipdr_conn_data[0:1])
                        (message_id,) = struct.unpack('!B', ipdr_conn_data[1:2])
                        print("Version: {}, Message_id: {}".format(version, message_id))

                    """manual check out all parameters from protocol documents
                    从MESSAGEID判断报文类型，处理TEMPLATE的内容用于后面的数据的解析"""
                    if message_id is 16:
                        print("This is session template packet, unpack for tem model......")
                        (session_id,) = struct.unpack('!B', ipdr_conn_data[2:3])
                        (message_flags,) = struct.unpack('!B', ipdr_conn_data[3:4])
                        print("Session_id: {}, Message_flags: {}".format(session_id, message_flags))

                        (message_length,) = struct.unpack('!L', ipdr_conn_data[4:8])
                        (config_id,) = struct.unpack('!h', ipdr_conn_data[8:10])
                        print("Message_length: {}, Config_id: {}".format(message_length, config_id))

                        (flags,) = struct.unpack('!B', ipdr_conn_data[10:11])
                        (template_id,) = struct.unpack('!L', ipdr_conn_data[11:15])
                        print("flags: {}, template_id: {}".format(flags, template_id))

                        (schemaname_type,) = struct.unpack('!L', ipdr_conn_data[15:19])
                        (schemaname_len,) = struct.unpack('!h', ipdr_conn_data[19:21])
                        print("schemaname_len: {}, schemaname: {}".format(schemaname_type, schemaname_len))

                        (schemaname,) = struct.unpack('!%ss' % schemaname_len, ipdr_conn_data[21:21 + schemaname_len])
                        ll = schemaname_len
                        ll += 21
                        (typename_len,) = struct.unpack('!L', ipdr_conn_data[ll:ll + 4])
                        ll += 4
                        print("schemaname: {}, typename_len: {}".format(schemaname, typename_len))

                        (typename,) = struct.unpack('!%ss' % typename_len, ipdr_conn_data[ll:ll + typename_len])
                        ll = ll + typename_len
                        (tem_num,) = struct.unpack('!L', ipdr_conn_data[ll:ll + 4])
                        ll += 4
                        print("typename: {}, tem_num: {}".format(typename, tem_num))

                        for tem in range(0, tem_num):
                            """IPDR Document: IPDR/XDR ENcoding Format, IPDR streaming protocol, 
                            CM-SP-OSSIV3.0-I14-110210                            
                            int 0x00000021
                            unsignedint 0x00000022
                            long    0x00000023
                            unsignedlong    0x00000024
                            float   0x00000025
                            double  0x00000026
                            hexBinary or base64Binary1  0x00000027

                            typeID:0x00000021
                            size in bytes:4

                            400 = 4 + x, 20 = 4 + 16"""
                            ipdr_arr = {'0x21': 4,
                                        '0x22': 4,
                                        '0x23': 8,
                                        '0x24': 8,
                                        '0x25': 4,
                                        '0x26': 8,
                                        '0x27': 400,
                                        '0x28': 400,
                                        '0x29': 1,
                                        '0x2a': 1,
                                        '0x2b': 1,
                                        '0x2c': 2,
                                        '0x2d': 2,
                                        '0x122': 4,
                                        '0x224': 8,
                                        '0x322': 4,
                                        '0x427': 20,
                                        '0x827': 20,
                                        '0x527': 20,
                                        '0x623': 8,
                                        '0x723': 8,
                                        }

                            for i in range(0, 3):
                                field = ['typeid', 'fieldid', 'fieldlen']
                                (meter_num,) = struct.unpack('!L', ipdr_conn_data[ll:ll + 4])
                                ll += 4
                                if i is 0:
                                    typeid = hex(meter_num)
                                    print("%s_hex: " % (field[i]), typeid)
                                    for key, value in ipdr_arr.items():
                                        if debug:
                                            print("key, value: ", key, value)
                                        if typeid == key:
                                            print("parameter_len: ", value)
                                            value_all.append(value)
                                    if debug:
                                        print("%s: " % (field[i]), meter_num)

                            (fieldName,) = struct.unpack('!%ss' % meter_num, ipdr_conn_data[ll:ll + meter_num])
                            ll = ll + meter_num
                            all_para.append(fieldName.decode(encoding='utf-8'))
                            print("fieldName: ", fieldName, ll)

                            (isenable,) = struct.unpack('!B', ipdr_conn_data[ll:ll + 1])
                            ll += 1
                            if debug:
                                print("isenable: ", isenable)
                            if message_length - ll < 14:
                                break
                            else:
                                continue
                        """从TEMPLATE里取TYPEID和参数"""
                        print("all_pa: {}".format(all_para))
                        print("all_para: {}".format(value_all))

                """最后再看下IPDR的交互是需要KEEP_ACK, DATA_ACK维持的，等有空再研究下，如果只是单纯的连接和接收数据已经可以了"""
                while True:
                    while True:
                        if self.netflow:
                            if debug:
                                print("{} socket running".format(self.axos_ip))
                            ipdr_gettem_data = self.netflow.recv(65535)
                            if debug:
                                print("getdata len:", len(ipdr_gettem_data))
                            if len(ipdr_gettem_data) > 0:
                                break
                            else:
                                """如果E7连接断了需要重新BING PC的PORT， 重新发送消息给E7，循环SESSION SET UP过程，
                                重启和切换都设置成360S，等待E7起来能够重新建立连接，
                                BING PC PORT需要不停的增加以避免端口占用出错，
                                断连以后需要再建立通道，IPDR中代码是用来做CLIENT的，没有LISTEN的功能，需要重新建立SOCKET"""
                                logging.warning("{} break, please wait 360s reconnection....".format(self.axos_ip))
                                print("self.netflow: ", self.netflow)
                                time.sleep(60)
                                self.netflow.close()
                                print("self.netflow_after: ", self.netflow)
                                time.sleep(300)
                                netflow_cc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                self.netflow = netflow_cc

                                print('axosip: ', self.axos_ip)
                                bindport = self.localport[1] + 2
                                self.localport[1] = self.localport[1] + 2

                                if self.netflow:
                                    print("{} reconnection {}....".format(self.localip, bindport))
                                    try:
                                        self.netflow.bind((self.localip, bindport))  # 重新固定本端的连接端口
                                    except ValueError as socket_error:
                                        print("binderror", socket_error)

                                    print("{} reconnection {}....".format(self.axos_ip, self.port))
                                    self.ipdrmain()

                                break
                            break
                        break

                    """解析MAC需要知道MAC从设备发出来是什么格式，是不是一定需要转ASCII， IPFIX需要转，IPDR不需要，直接是16进制"""
                    ipdr_temp = ipdr_gettem_data
                    if debug:
                        if ipdr_temp[221:len(ipdr_temp)]:
                            print("\r\nipd: ", len(ipdr_temp), ipdr_temp)
                            for ipd in ipdr_temp[72:80]:
                                if debug:
                                    print("ipd_head:", len(ipdr_temp), type(ipdr_temp), type(ipd))
                                print([hex(ipd)][0].replace('0x', ''), end=':')
                            print("\r\n")

                    if ipdr_gettem_data:
                        if debug:
                            print('\r\ripdr_gettem_data:', len(ipdr_gettem_data),
                                  ipdr_gettem_data[0:len(ipdr_gettem_data)])
                            for ipd in ipdr_temp[0:len(ipdr_gettem_data)]:
                                print([hex(ipd)][0].replace('0x', ':'), end='')
                            print("\r\n")
                        # Unpack the string
                        (version,) = struct.unpack('!B', ipdr_gettem_data[0:1])
                        (message_id,) = struct.unpack('!B', ipdr_gettem_data[1:2])
                        print("\n{}-Version: {}, Message_id: {}".format(self.axos_ip, version, message_id))

                        if version is 2:
                            if message_id is 8:
                                print("This is session start packet, no unpack......")

                            elif message_id is 64:
                                print("This is session keep_alive packet, no unpack......")

                            elif message_id is 16:
                                print("This is session template_data packet, need unpack it first......")

                            elif message_id is 32:
                                (session_id,) = struct.unpack('!B', ipdr_gettem_data[2:3])
                                (message_flags,) = struct.unpack('!B', ipdr_gettem_data[3:4])
                                print("Session_id: {}, Message_flags: {}".format(session_id, message_flags))

                                (message_length,) = struct.unpack('!L', ipdr_gettem_data[4:8])
                                (template_id,) = struct.unpack('!h', ipdr_gettem_data[8:10])
                                print("Message_length: {}, Template_id: {}".format(message_length, template_id))

                                (config_id,) = struct.unpack('!h', ipdr_gettem_data[10:12])
                                (flags,) = struct.unpack('!B', ipdr_gettem_data[12:13])
                                print("Config_id: {}, Flags: {}".format(config_id, flags))

                                (sequence_number,) = struct.unpack('!Q', ipdr_gettem_data[13:21])
                                (ipdr_data_len,) = struct.unpack('!L', ipdr_gettem_data[21:25])
                                print("Sequence_number: {}, Ipdr_total_len: {}".format(sequence_number, ipdr_data_len))
                                mm = 25

                                for aa, bb in zip(all_para, value_all):
                                    if debug:
                                        print("ipdr: {} : {}".format(aa, int(bb)))

                                    """用参数的长度来分类怎么解析，参数对应的长度需要从协议文档里找TYPEID手工列表
                                    TYPEID可以从TEMPLATE报文里解析出来，再取长度的列表"""
                                    if int(bb) == 1:
                                        (Service_len,) = struct.unpack('!B', ipdr_gettem_data[mm:mm + 1])
                                        print("{}: {}".format(aa, Service_len))
                                        mm += 1

                                    elif int(bb) == 4:
                                        (hostname,) = struct.unpack('!L', ipdr_gettem_data[mm:mm + 4])
                                        if 'v4' in aa:
                                            a = long2ip(hostname)
                                            print("{}: {}".format(aa, a))

                                        elif 'Time' in aa:
                                            gettime(hostname, aa)

                                        else:
                                            print("{}: {}".format(aa, hostname))
                                        mm = mm + 4

                                    elif int(bb) == 8:
                                        if 'Mac' in aa:
                                            print("{}: ".format(aa), end='')
                                            for ipd in ipdr_temp[mm:mm + 8]:
                                                print([hex(ipd)][0].replace('0x', ':'), end='')
                                            if debug:
                                                print('\r')
                                            mm = mm + 8
                                        elif 'Service' in aa:
                                            (packets,) = struct.unpack('!q', ipdr_gettem_data[mm:mm + 8])
                                            print("{}: {}".format(aa, packets))
                                            mm = mm + 8
                                        else:
                                            if debug:
                                                print("aa, mm: ", aa, mm)
                                            for cc in range(0, 2):
                                                (createtime,) = struct.unpack('!L', ipdr_gettem_data[mm:mm + 4])
                                                gettime(createtime, aa)
                                                mm = mm + 4

                                    else:
                                        (hostlen,) = struct.unpack('!L', ipdr_gettem_data[mm:mm + 4])
                                        if debug:
                                            print("hostlen: ", hostlen)
                                        mm += 4

                                        (hostname,) = struct.unpack('!%ss' % hostlen, ipdr_gettem_data[mm:mm + hostlen])
                                        print("{}: ".format(aa), hostname)
                                        if 'v6' in aa:
                                            a = dec2ipv6(str(hostname, encoding='utf-8'))
                                            if a:
                                                print("{}: {}".format(aa, a))
                                                dec2ipv6('281473913978881')
                                                print("hostname: ", str(hostname, encoding='utf-8'))
                                        mm = mm + hostlen

                        if self.netflow:
                            self.netflow.send(ipdr_keep_data[0])
                            self.netflow.send(ipdr_data_ack[0])
                        if not ipdr_gettem_data:
                            continue
                    else:
                        continue

                print("IPDR process out of services...................................")
                time.sleep(5)


def mainrun():
    """为了断连以后重新连接，把SOCKET建立连接部分单独提出来用于调用
    线程中断连接以后，重新建立SOCKET，BIND LOCALPORT，再和E7重新建立SESSION"""
    while localip:
        netflow_aa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        netflow_bb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        netflow = [netflow_aa, netflow_bb]

        for ip, netflow_sock in zip(axos_ip, netflow):
            """同时起二个线程，不需要用到主线程的逻辑关系，用APPEND写成一个主线程二个子线程
            也可以写成同时起二个主线程
            也可以同时起二个进程，暂时没用
            目前只支持IPV4，IPV6有代码但是还没有处理过"""
            if netflow_sock is netflow_aa:
                port = localport[0]
            elif netflow_sock is netflow_bb:
                port = localport[1]
            print("ip, port: ", ip, port)
            netflow_sock.bind((localip, port))  # 必须固定本端的连接端口才能让E7连接到对应的端口通信，本地是CLIENT
            t = threading.Thread(target=Ipdrrun, args=(netflow_sock, ipdr_port, ip, localip, localport), daemon=True)
            threads.append(t)

        """启动线程,逐个加入并行启动"""
        for i in loop:
            threads[i].start()
        for i in loop:
            threads[i].join()

        if debug:
            print("threading: ", threading.enumerate())
            print("threading_active: ", threading.active_count())


if __name__ == "__main__":
    '''change by Maojun Wang
    root@GPON-8R2_sean:~# netstat -anp |grep 4737
    tcp        0      0 0.0.0.0:4737            0.0.0.0:*               LISTEN      12837/ipdrd     
    tcp        0      0 10.245.46.218:4737      10.245.251.33:40069     TIME_WAIT   -               
    tcp        0      0 10.245.46.218:4737      10.245.251.33:41682     TIME_WAIT   -               
    tcp        0      0 10.245.46.218:4737      10.245.251.33:36007     TIME_WAIT   -               
    udp        0      0 0.0.0.0:4737            0.0.0.0:*                           12837/ipdrd     
    root@GPON-8R2_sean:~# '''
    iplist = []
    threads = []
    port = 0
    axos_ip = ['10.245.46.226', '10.245.46.218']
    # axos_ip = ['10.245.46.223',]
    localip = socket.gethostbyname(socket.gethostname())
    localport = [40516, 40517]
    # localport = [40516, ]
    ipdr_port = 4737
    loop = range(len(axos_ip))
    print("loop:", loop)
    mainrun()

"""DOCSIS SAMIS Type 1 IPDR records contain the following CMTS attributes:
 CmtsHostName
 CmtsSysUpTime
 CmtsIpv4Addr
 CmtsIpv6Addr
 CmtsMdIfName
 CmtsMdIfIndex

DOCSIS SAMIS Type 2 IPDR records contain the following CMTS attributes:
 CmtsHostName
 CmtsSysUpTime
 CmtsMdIfName
 CmtsMdIfIndex

DOCSIS SAMIS Type 1 IPDR records contain the following CM attributes:
 CmMacAddr
 CmIpv4Addr
 CmIpv6Addr
 CmIpv6LinkLocalAddr
 CmQosVersion
 CmRegStatusValue
 CmLastRegTime

DOCSIS SAMIS Type 2 IPDR records contain the following CM attributes:
 CmMacAddr

Category Attribute Name Type Presence Permitted Values
Who CmtsHostName String Required FQDN
When CmtsSysUpTime unsignedInt Required nnnnnnnnn
Who CmtsIpv4Addr ipV4Addr Required nnn.nnn.nnn.nnn
Who CmtsIpv6Addr ipV6Addr Required xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx
What CmtsMdIfName String Required SIZE (0..50)
What CmtsMdIfIndex unsignedInt Required nnnnnnnnn"""
