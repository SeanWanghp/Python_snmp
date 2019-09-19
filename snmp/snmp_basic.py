from pysnmp.hlapi.asyncore import *


class PsnmpLib(object):

    def __init__(self):
        self.snmpEngine = SnmpEngine()
        pass

    @staticmethod
    def cbFun_v2(snmpEngine, sendRequestHandle, errorIndication,
              errorStatus, errorIndex, varBinds, cbCtx):
        if errorIndication:
            print(errorIndication)
            return
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBindTable[-1][int(errorIndex) - 1][0] or '?'))
            return
        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))

    @staticmethod
    def cbFun_v3(snmpEngine, sendRequestHandle, errorIndication,
              errorStatus, errorIndex, varBindTable, cbCtx):
        '''this CBFUN is using for SNMPv3, can not using for SNMPv2'''
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

    def v2_getcmd(self):
        getCmd(self.snmpEngine,
               CommunityData('public'),
               UdpTransportTarget(('demo.snmplabs.com', 161)),
               ContextData(),
               ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)),
               cbFun=self.cbFun_v2)

        self.snmpEngine.transportDispatcher.runDispatcher()

    def v3_getcmd(self):
        getCmd(self.snmpEngine,
               UsmUserData('jie_auth_no', '12345678'),
               UdpTransportTarget(('10.245.46.208', 161), timeout=30, retries=2),
               ContextData(),
               ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)),
               cbFun=self.cbFun_v2)
        self.snmpEngine.transportDispatcher.runDispatcher()

    def v3_walkcmd(self):
        nextCmd(self.snmpEngine,
                UsmUserData('jie_auth_no', '12345678', None),
                UdpTransportTarget(('10.245.46.208', 161), timeout=30, retries=2),
                ContextData(),
                # ObjectType(ObjectIdentity('SNMPv2-MIB', 'system')),
                ObjectType(ObjectIdentity('IF-MIB', 'ifTable')),
                cbFun=self.cbFun_v3)
        self.snmpEngine.transportDispatcher.runDispatcher()


if __name__ == '__main__':
    sn = PsnmpLib()
    sn.v2_getcmd()
    sn.v3_getcmd()
    sn.v3_walkcmd()
