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
# from pysnmp.entity.rfc3413.oneliner import cmdgen
# from pysnmp.entity import engine
from os.path import exists
import sys, os, datetime, time, multiprocessing, telnetlib, subprocess, string, logging, datetime, random
from time import sleep
import re as sre
from multiprocessing import Process
from pysnmp.hlapi.asyncore import *


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
# def cbFun(snmpEngine, sendRequestHandle, errorIndication,
#           errorStatus, errorIndex, varBinds, cbCtx):
#     if errorIndication:
#         print(errorIndication)
#         return
#     elif errorStatus:
#         print('%s at %s' % (errorStatus.prettyPrint(),
#                             errorIndex and varBindTable[-1][int(errorIndex) - 1][0] or '?'))
#         return
#     else:
#         for varBind in varBinds:
#             print(' = '.join([x.prettyPrint() for x in varBind]))
#
#
# snmpEngine = SnmpEngine()
#
# getCmd(snmpEngine,
#        CommunityData('public'),
#        UdpTransportTarget(('10.245.46.213', 161)),
#        ContextData(),
#        ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)),
#        cbFun=cbFun)
#
# snmpEngine.transportDispatcher.runDispatcher()


class SNMP_pysnmp(object):
    def __init__(self, snmp_community, ip, snmp_port):
        self.snmpEngine = SnmpEngine()
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
        print("********************getcmd*************************")
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
        print("********************netxcmd*************************")
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
        print("********************bulkCmd*************************")
        bulkCmd(self.snmpEngine,
                CommunityData(self.snmp_community),
                UdpTransportTarget((self.ip, self.snmp_port), timeout=30, retries=2),#SNMP timeout setting for E7-20
                ContextData(),
                0, 25,
                ObjectType(ObjectIdentity('SNMPv2-MIB', 'system')),
                cbFun=self.cbFun)
        return self.snmpEngine.transportDispatcher.runDispatcher()

    # def snmpTrap(self):
    #
    #     errorIndication, errorStatus, errorIndex, varBinds = next(
    #         sendNotification(
    #             SnmpEngine(),
    #             CommunityData('public', mpModel=0),
    #             UdpTransportTarget(('demo.snmplabs.com', 162)),
    #             ContextData(),
    #             'trap',
    #             NotificationType(
    #                 ObjectIdentity('1.3.6.1.6.3.1.1.5.2')
    #             ).addVarBinds(
    #                 (b'1.3.6.1.6.3.1.1.4.3.0', b'1.3.6.1.4.1.20408.4.1.1.2'),
    #                 ('1.3.6.1.2.1.1.1.0', OctetString('my system'))
    #             )
    #         )
    #     )
    #
    #     if errorIndication:
    #         print(errorIndication)


# from pysnmp.hlapi import *
class SNMPv3_py(object):

    def __init__(self, snmpv3_community, snmpv3_host, snmpv3_port):
        self.snmp_community = snmpv3_community
        self.host = snmpv3_host
        self.port = snmpv3_port
        pass

    def snmpv3_next(self):
        # noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
        def cbFun(snmpEngine, sendRequestHandle, errorIndication,
                  errorStatus, errorIndex, varBindTable, cbCtx):
            if errorIndication:
                print(errorIndication)
                return
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBindTable[-1][int(errorIndex) - 1][0] or '?'))
                return
            else:
                for varBindRow in varBindTable:
                    for varBind in varBindRow:
                        print(' = '.join([x.prettyPrint() for x in varBind]))

            return True  # request lower layers to do GETNEXT and call us back

        snmpEngine = SnmpEngine()

        nextCmd(snmpEngine,
                UsmUserData(self.snmp_community, '12345678'),
                UdpTransportTarget((self.host, 161)),
                ContextData(),
                ObjectType(ObjectIdentity('SNMPv2-MIB', 'system')),
                ObjectType(ObjectIdentity('IF-MIB', 'ifTable')),
                cbFun=cbFun)

        snmpEngine.transportDispatcher.runDispatcher()


if __name__ == '__main__':
    snmp_community = 'public'
    ip = '10.245.46.216'
    snmp_port = 161
    snmp_run_v2 = SNMP_pysnmp(snmp_community, ip, snmp_port)
    cmd = ['getcmd', 'nextcmd', 'bulkcmd']
    cm = cmd[0]
    if cm is cmd[0]:
        snmp_run_v2.bulkcmd()
    elif cm is cmd[1]:
        snmp_run_v2.nextcmd()
    elif cm is cmd[2]:
        snmp_run_v2.getcmd()
    snmpv3_community = 'jie_auth_no'
    snmpv3_host = '10.245.46.208'
    snmp_run_v3 = SNMPv3_py(snmpv3_community, snmpv3_host, snmp_port)
    snmp_run_v3.snmpv3_next()
