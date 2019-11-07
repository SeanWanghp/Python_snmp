# coding=utf-8                                                                  #this must be in first line
#C:\Python27\Doc python
__author__='Sean Wang'
#data@:2017-03-27
#update data@:2019-01-28
# coding=gbk                                                                    #spell inspection cancelled
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word
####window用户在C:\Users\yourusername\PySNMP Configuration\mibs下
####linux用户在~/.pysnmp/mibs下
####Danjgo web:    https://www.cnblogs.com/xuyiqing/p/8274912.html
####https://www.cnblogs.com/cate/python/
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.entity import engine
from os.path import exists
import sys, os, datetime, time, multiprocessing, telnetlib, subprocess, string, logging, datetime, random
from time import sleep
import re as sre
from multiprocessing import Process
from pysnmp.smi import builder
from pysnmp.proto import rfc1155, rfc1902, api
from pyasn1.codec.ber import encoder, decoder
import logging

#open debug cmd
# from pysnmp.debug import setLogger,Debug
# setLogger( Debug('all'))


class Pysnmpmib(object):
    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        for mib_path in builder.MibBuilder().getMibSources():
            print("original mib_path: {}".format(mib_path))
        return object.__new__(cls, *args, **kwargs)


class _Gen(Pysnmpmib):

    def __init__(self):
        super(_Gen, self).__init__()
        # Check for already existing file
        # target_file_name = str(random.random()) + '.txt'
        self.target_file_name = '1.txt'
        self.community_name = 'public'

        # Initialize counter to zero
        self.counter = 0

        # Create command generator
        self.engine = engine.SnmpEngine()
        self.gen = cmdgen
        self.cmdgen = self.gen.CommandGenerator(self.engine)
        self.build = builder.MibBuilder()
        # self.add_personal_mib()

    def add_personal_mib(self):
        '''
        增加LIB的方法，写的很详细，角本中的BUILD和例子中的有区别，注意库的引用有所不同
        https://programtalk.com/vs2/python/11801/sd-agent/checks.d/snmp.py/
        '''
        mibs_path = 'C:\\robot\\'
        # print mibs_path
        if mibs_path:
            mib_sources = self.build.getMibSources() + (builder.DirMibSource(mibs_path),)
            # print "mib_sources: ", mib_sources
            self.build.setMibSources(*mib_sources)
        for mib_path in self.build.getMibSources():
            logging.warning("mibsource add path: {}".format(mib_path))

    def log_path(self):
        path = 'snmp_walk_result/'
        # if not os.path.exists(path):
        #     os.makedirs(path)
        # if exists(path + target_file_name):
        #     sys.exit("The file '%s' already exists. Try again." % target_file_name)
        # else:
        #     # target_file = open(path + target_file_name, 'w+')
        pass

    def _Gen_get(self, target_IP, target_port):
        '''
        GET的方法输出和NEXT, BULK有所区别,所以需要用不同的方法输出OID的值
        '''
        oid_id = '.1.3.6.1.2.1.1.1.0'
        oid_id_1 = '.1.3.6.1.2.1.1.2.0'
        print("target_IP", target_IP, target_port, self.target_file_name)

        # Get data
        errorIndication, errorStatus, errorIndex, varBinds = self.cmdgen.getCmd(
            self.gen.CommunityData(self.community_name),
            self.gen.UdpTransportTarget((target_IP, target_port), timeout=10, retries=0),  #SNMP get timeout
            oid_id,
            oid_id_1
        )
        for value_var in varBinds:
            print('varBinds: ', value_var)

        # self._Log_snmp(errorIndication, errorStatus, errorIndex, varBinds)

    def _Gen_next(self, target_IP, target_port):
        # Turn on debugging
        # debug.setLogger(debug.Debug('msgproc', 'secmod'))
        oid_id = '1.3.6.1'
        print("target_IP", target_IP, target_port, self.target_file_name)

        # Get data
        errorIndication, errorStatus, errorIndex, varBindTable = self.cmdgen.nextCmd(
            self.gen.CommunityData(self.community_name),
            self.gen.UdpTransportTarget((target_IP, target_port), timeout=10, retries=0),
            oid_id,  # <----------------- doesn't seem perfect either
            lexicographicMode=True,
            maxRows=5,  # <-------------------- can't leave it out
            ignoreNonIncreasingOid=True,
            lookupNames=True,
            lookupValues=True
        )
        self._Log_snmp(errorIndication, errorStatus, errorIndex, varBindTable)

    def _Gen_bulk(self, target_IP, target_port):
        oid_id = '1.3.6.1'
        print("target_IP", target_IP, target_port, self.target_file_name)

        # Get data
        errorIndication, errorStatus, errorIndex, varBindTable = self.cmdgen.bulkCmd(
            self.gen.CommunityData(self.community_name),
            self.gen.UdpTransportTarget((target_IP, target_port), timeout=10, retries=0),
            0, 25,
            oid_id,  # <----------------- doesn't seem perfect either
            lexicographicMode=True,
            maxRows=5000,  # <-------------------- can't leave it out
            ignoreNonIncreasingOid=True,
            lookupNames=True,
            lookupValues=True
        )
        self._Log_snmp(errorIndication, errorStatus, errorIndex, varBindTable)

    def _Log_snmp(self, errorIndication, errorStatus, errorIndex, varBindTable):
        '''
        四个值在库里可以查看原始参数,本方法是给NEXT和BULK提供OID值的输出, GET需要用不同方法
        :param errorIndication:
        :param errorStatus:
        :param errorIndex:
        :param varBindTable:
        :return:
        '''
        # Print errors and values to file
        if errorIndication:
            print(errorIndication)
        else:
            # Print error messages
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex) - 1] or '?'
                )
                      )
            else:
                # Print values
                for varBindTableRow in varBindTable:
                    for name, val in varBindTableRow:
                        self.counter += 1
                        # target_file.write("(%s)\t start_OID: %s\tvalue =\t%s\n" % (self.counter, name.prettyPrint(), val.prettyPrint()))
                        print(self.counter, name.prettyPrint(), val.prettyPrint())

                # Finish the operation
                # target_file.close()
                # print('Writing to %s successful. %d lines have been written' % (target_file_name, self.counter))
                # sys.exit(0)


class Runwalk:
    def __init__(self):
        # self.run = _Gen()
        pass

    def run_bulk(self, target_IP, target_port):
            self.run = _Gen()
            cmd = ['getcmd', 'nextcmd', 'bulkcmd']
            cm = cmd[0]

            if cm is cmd[0]:
                return self.run._Gen_bulk(target_IP, target_port)
            elif cm is cmd[1]:
                return self.run._Gen_next(target_IP, target_port)
            elif cm is cmd[2]:
                return self.run._Gen_get(target_IP, target_port)


def main(msg, tel_port, wait_time):
    ff = Runwalk()
    for i in range(1, 2):
        for wait in range(0, wait_time):
            '''
            多进程调用会比较快,但是同时会过多的占用CPU,有利有弊
            换线程调用,CPU利用率会低,但同时运行速度也会变慢,在数量少的情况下还是用进程比较好
            '''
            logging.warning(f"SNMP start at the {wait+1} times, total loop times is {wait_time}")
            pool = multiprocessing.Pool(processes=len(msg))
            for (ip, port) in zip(msg, tel_port):
                pool.apply_async(ff.run_bulk, args=(ip, port))    #thread running on E7,,,also can using: pool.apply()
                # pool.apply_async(_run_walk(ip, port))  # will run step by step
            pool.close()
            pool.join()
        logging.warning(f"***********************SNMP walking done {wait_time} times**********************")


if __name__ == '__main__':
    GE24_ip = '10.245.46.207'
    Gpon8_ip = '10.245.46.208'
    TenGE12_ip = '10.245.46.223'
    NGPON2_ip = '10.245.46.216'
    port = '161'
    # msg = [ip, ip, ip, ip, ip]
    msg = [GE24_ip, Gpon8_ip, TenGE12_ip, NGPON2_ip]
    # tel_port = [port, port, port, port, port]
    tel_port = ['161', port, port, port]
    wait_time = 9999
    main(msg, tel_port, wait_time)

