# --encoding=UTF-8--
# coding=gbk
__author__ = 'Maojun Wang'

# from ncclient import manager
# HOST = '10.245.46.208'
# PORT = 830
# USERNAME = 'sysadmin'
# PASSWORD = 'sysadmin'
#
# client = manager.connect(host=HOST, port=PORT, username=USERNAME, password=PASSWORD)
# print(client.connected)
#
# reply = client.send_rpc('<initialize><tape-content>110111</tape-content></initialize>')
# print(reply)

import paramiko
import socket
import time
import sys

"""http://rtodto.net/how-to-upgrade-junos-remotely-via-netconf/"""

Send_XML = """
<?xml version="1.0" encoding="UTF-8"?>
<rpc message-id="106" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
   <get-config>
        <source>
          <running/>
        </source>
        <filter>
            <Configuration>
                <InterfaceConfigurationTable/>
            </Configuration>
        </filter>
      </get-config>
 </rpc>
]]>]]>"""

VERSION = """
<rpc message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <get xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
      <filter type="xpath" select="/status/system/version"/>
    </get>
</rpc>
]]>]]>"""

CONFIG = """
<rpc message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <get-config>
    <source>
      <running/>
    </source>
  </get-config>
</rpc>
]]>]]>"""

HELLO = """
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>"""

SendXML = """
<rpc message-id="102" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="">
  <get>
    <filter xmlns:t="http://www.caxxx.com/ns/exa/base" type="xpath"
            select="/status/system/discovered-onts"/>
  </get>
</rpc>
]]>]]>"""

CLOSESESSION = """
<rpc message-id="110">
  <close-session/>
</rpc>
]]>]]>"""

E720 = """
<rpc message-id="97" nodename="" timeout="3">
<action><action-type>show-ont-port-color</action-type><action-args/></action>
</rpc>
]]>]]>"""

ONTPORT = """<rpc message-id="{}" nodename="" timeout="30"><action><action-type>show-ont-port-color</action-type>
<action-args><after><object>{}-3-1</object></after></action-args></action></rpc>
"""

AXOSYANG = [HELLO, VERSION, Send_XML, CONFIG, CLOSESESSION]


class Netconf_Object:
    def __init__(self):
        # self.ROUTER_IP = '10.245.46.216'
        self.ROUTER_IP = '10.245.48.60'
        self.PORT = 830
        # self.USERNAME = 'sysadmin'
        # self.PASSWORD = 'seanwang'
        self.USERNAME = 'e7'
        self.PASSWORD = 'admin'
        self.netconf_login()
        self.netconf_sendcommand()

    def netconf_login(self):
        try:
            self.trans = paramiko.Transport((self.ROUTER_IP, self.PORT))
            self.trans.connect(username=self.USERNAME, password=self.PASSWORD)
        except Exception as e:
            raise SSHException

        # CREATE CHANNEL FOR DATA COMM
        self.ch = self.trans.open_session()
        # self.name = self.ch.set_name('netconf')

        # Invoke NETCONF, define using NETCONF protocol
        self.ch.invoke_subsystem('netconf')

    def netconf_sendcommand(self):
        # SEND COMMAND
        for i in range(1, 2076, 37):
            print(i)
            self.ch.send(ONTPORT.format(i, str(10000+i)))
            data = self.ch.recv(99999)
            for da in [data]:
                print("da:", da.decode('utf-8'))

        # for yang in AXOSYANG:
        #     self.ch.send(yang)
        #     data = self.ch.recv(99999)
        #     for da in [data]:
        #         print("da:", da.decode('utf-8'))
                # if data.find(b'</rpc-reply>]]>]]>'):
                # if data.find(b'') != -1:
                # We have reached the end of reply
            print('Netconf responding finsished..........................................')
            time.sleep(1)   # E7 need time respond netconf request

        # else:
        #     print('Netconf responding finsished')
        self.ch.close()

    # def __del__(self):
    #     self.ch.close()
    # self.trans.close()
    # self.socket.close()

    def sftpclient(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.trans = paramiko.Transport((self.ROUTER_IP, self.PORT))
        self.ssh.get_transport = self.trans

        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.connect((self.ROUTER_IP, self.PORT))

        # SFTP transfer files
        sftp = paramiko.SFTPClient.from_transport(self.trans)
        # put location.py to server /tmp/test.py
        sftp.put('/tmp/location.py', '/tmp/test.py')
        # get remove_path to local local_path
        sftp.get('remove_path', 'local_path')


Netconf_Object()
