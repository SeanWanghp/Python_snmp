# --encoding=UTF-8--
# coding=gbk
__author__ = 'Maojun Wang'
# import modeled.netconf
# from netconf.client import NetconfSSHSession
# HOST = '10.245.46.207'
# PORT = 830
# USERNAME = 'sysadmin'
# PASSWORD = 'sysadmin'
#
# client = NetconfSSHSession(HOST, port=PORT, username=USERNAME, password=PASSWORD)
#
# reply = client.send_rpc('<initialize><tape-content>110111</tape-content></initialize>')
# print reply



import paramiko
import socket
import time, sys
###############http://rtodto.net/how-to-upgrade-junos-remotely-via-netconf/#################

ROUTER_IP = '10.245.46.216'
PORT = 830
USERNAME = 'sysadmin'
PASSWORD = 'sysadmin'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

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

HELLO ="""
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>"""

Send_XML = """
<rpc message-id="102" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="">
  <get>
    <filter xmlns:t="http://www.calix.com/ns/exa/base" type="xpath"
            select="/status/system/discovered-onts"/>
  </get>
</rpc>
]]>]]>"""

CLOSE = """
<rpc message-id="110">
  <close-session/>
</rpc>
]]>]]>"""

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((ROUTER_IP, PORT))

trans = paramiko.Transport(socket)
trans.connect(username=USERNAME, password=PASSWORD)

# CREATE CHANNEL FOR DATA COMM
ch = trans.open_session()
name = ch.set_name('netconf')

# # Invoke NETCONF
ch.invoke_subsystem('netconf')

# SEND COMMAND
ch.send(HELLO)

# ch.send(Send_XML)
ch.send(VERSION)
# ch.send(CONFIG)

# Recieve data returned
data = ch.recv(2048)
while data:
    data = ch.recv(1024)
    for da in [data]:
        print "da:", da
    if data.find('</rpc-reply>]]>]]>') != 0:
    # if data.find('') != -1:
        # We have reached the end of reply
        ch.send(CLOSE)
        print 'yang finsished..........................................'

else:
    print 'bbbbbbbbbbbbbbbbbb'


ch.close()
trans.close()
socket.close()