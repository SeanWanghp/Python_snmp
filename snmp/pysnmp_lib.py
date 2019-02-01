# coding=utf-8                                                                  #this must be in first line
#C:\Python27\Doc python
__author__='Sean Wang'
#data@:2017-03-27
#update data@:2019-01-28
# coding=gbk                                                                    #spell inspection cancelled
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word

####Danjgo web:    https://www.cnblogs.com/xuyiqing/p/8274912.html
####https://www.cnblogs.com/cate/python/
# coding=utf-8
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.entity import engine
from os.path import exists
import sys, os, datetime, time, multiprocessing, telnetlib, subprocess, string, logging, datetime, random
from time import sleep
import re as sre
from multiprocessing import Process
from pysnmp.hlapi.asyncore import *


class SNMP_pysnmp():
    def __init__(self, snmpEngine, snmp_community, ip, snmp_port):
        self.snmpEngine = snmpEngine
        self.snmp_community = snmp_community
        self.ip = ip
        self.snmp_port = snmp_port

    def engine_run(self, engine):
        return engine.transportDispatcher.runDispatcher()

    # noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
    def cbFun(self, snmpEngine, sendRequestHandle, errorIndication, errorStatus, errorIndex, varBinds, cbCtx):
        if errorIndication:
            print(errorIndication)
            return
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[-1][int(errorIndex) - 1][0] or '?'))
            return
        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))
        return True  # request lower layers to do GETNEXT and call us back

    def getcmd(self):
        print "********************getcmd*************************"
        getCmd(self.snmpEngine,       ################get value
           CommunityData(self.snmp_community),
           UdpTransportTarget((self.ip, self.snmp_port)),
           ContextData(),
           ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)),
           ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysObjectID', 0)),
           ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysUpTime', 0)),
           ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysContact', 0)),
           ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0)),
           ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysLocation', 0)),
           ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysServices', 0)),

           cbFun=self.cbFun)
        return self.engine_run(self.snmpEngine)

    def nextcmd(self):
        print "********************netxcmd*************************"
        nextCmd(self.snmpEngine,
                CommunityData(self.snmp_community),
                UdpTransportTarget((self.ip, self.snmp_port)),
                ContextData(),
                ObjectType(ObjectIdentity('IF-MIB', 'ifTable')),
                ObjectType(ObjectIdentity('IF-MIB', 'ifIndex')),
                ObjectType(ObjectIdentity('IF-MIB', 'ifDescr')),
                cbFun=self.cbFun)
        return self.engine_run(self.snmpEngine)

    def bulkcmd(self):
        print "********************bulkCmd*************************"
        bulkCmd(self.snmpEngine,
                CommunityData(self.snmp_community),
                UdpTransportTarget((self.ip, self.snmp_port), timeout=30, retries=2),#SNMP timeout setting for E7-20
                ContextData(),
                0, 25,
                ObjectType(ObjectIdentity('SNMPv2-MIB', 'system')),
                cbFun=self.cbFun)
        return self.engine_run(self.snmpEngine)


if __name__ == '__main__':
    snmpEngine = SnmpEngine()
    snmp_community = 'public'
    ip = '10.245.46.216'
    snmp_port = 161
    snmp_run_v2 = SNMP_pysnmp(snmpEngine, snmp_community, ip, snmp_port)
    cmd = ['getcmd', 'nextcmd', 'bulkcmd']
    cm = cmd[0]
    if cm is cmd[0]:
        snmp_run_v2.bulkcmd()
    elif cm is cmd[1]:
        snmp_run_v2.nextcmd()
    elif cm is cmd[2]:
        snmp_run_v2.getcmd()

