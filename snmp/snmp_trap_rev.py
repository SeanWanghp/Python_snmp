# coding=utf-8                                                                  #this must be in first line
__author__ = 'Maojun'
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
import socket
import sys
"""soure code from following web: 
http://snmplabs.com/pysnmp/examples/v3arch/asyncore/manager/ntfrcv/transport-tweaks.html
#receive-notifications-noting-peer-address
using following command to send trap:
snmptrap -v2c -c public 127.0.0.1:162 123 1.3.6.1.6.3.1.1.5.1 1.3.6.1.2.1.1.5.0 s test
using following command to recv snmptrap as above"""


class Snmptraprcv:
    def __init__(self, hosta, hostb, porta=162, portb=162):
        self.hosta = hosta
        self.hostb = hostb
        self.porta = porta
        self.portb = portb
        self.traprcv()

    def traprcv(self):
        """Create SNMP engine with autogenernated engineID and pre-bound to socket transport dispatcher"""
        snmpEngine = engine.SnmpEngine()

        """Transport setup  # UDP over IPv4, first listening interface/port"""
        config.addTransport(
            snmpEngine,
            udp.domainName + (1,),
            udp.UdpTransport().openServerMode((self.hosta, self.porta))
        )

        """UDP over IPv4, second listening interface/port"""
        config.addTransport(
            snmpEngine,
            udp.domainName + (2,),
            udp.UdpTransport().openServerMode((self.hostb, self.portb))
        )

        """SNMPv1/2c setup # SecurityName <-> CommunityName mapping"""
        config.addV1System(snmpEngine, 'my-area', 'public')

        """Register SNMP Application at the SNMP engine"""
        ntfrcv.NotificationReceiver(snmpEngine, self.cbFun)
        """this job would never finish"""
        snmpEngine.transportDispatcher.jobStarted(1)

        """Run I/O dispatcher which would receive queries and send confirmations"""
        try:
            snmpEngine.transportDispatcher.runDispatcher()
        except IOError:
            snmpEngine.transportDispatcher.closeDispatcher()
            raise
        finally:
            pass

    def cbFun(self, snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):
        """Callback function for receiving notifications
        #noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal"""
        print('Notification from ContextEngineId "%s", ContextName "%s"' %
              (contextEngineId.prettyPrint(), contextName.prettyPrint()))
        for name, val in varBinds:
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))

    def sockrcv(self):
        """this is socket way for SNMP listen
        http://snmplabs.com/pysnmp/examples/v3arch/asyncore/contents.html#notification-receiver-applications"""
        port = 162
        sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sk.bind(('', port))
        while 1:
            data, addr = sk.recvfrom(4048)
            print(data)


if __name__ == '__main__':
        rcv = Snmptraprcv('192.168.37.49', '127.0.0.1')
        # rcv.sockrcv()
