from MaojunLibrary.MobileAppLibrary import MobileAppLibrary
from MaojunLibrary.WebAppLibrary import WebAppLibrary
from MaojunLibrary.SshLibrary import SshLibrary
from MaojunLibrary.SnmpLibrary import SnmpLibrary
import sys
import socket
import re
import os
import copy
import time

class App(object):
    def __init__(self):
        pass

    def App_click_element(cls, locator):
        '''
        [Arguments]    ${locator}    ${selected}    ${timeout} =${30}
        [Documentation]
        ...
        Keyword: check_element
        ...
        ArgSpec(args=['self', 'locator', 'selected', 'timeout'], varargs=None, keywords=None, defaults=(30,))
        [Tags] @author = Sean W
        '''
        return MobileAppLibrary().click_element(locator)


class App_Snmp(object):
    def __init__(self):
        pass

    def App_snmp_connection(self, ip, port, community, version):
        self.snmp = SnmpLibrary(ip, port, community, version)

    def App_snmp_get(cls, oid):
        '''
        [Arguments]    ${ip}    ${port}    ${community} =${public}  ${version} ${oid}
        [Documentation]
        ...
        Keyword: check_element
        ...
        ArgSpec(args=['ip', 'port', 'community', 'version'], varargs=None, keywords=None, defaults=(30,))
        [Tags] @author = Sean W
        '''
        return cls.snmp.snmp_get(oid)

    def App_snmp_bulk(cls, oid):
        '''
        [Arguments]    ${ip}    ${port}    ${community} =${public}  ${version} ${oid}
        [Documentation]
        ...
        Keyword: check_element
        ...
        ArgSpec(args=['ip', 'port', 'community', 'version'], varargs=None, keywords=None, defaults=(30,))
        [Tags] @author = Sean W
        '''
        return cls.snmp.snmp_bulk(oid)

    def App_snmp_next(cls, oid):
        '''
        [Arguments]    ${ip}    ${port}    ${community} =${public}  ${version} ${oid}
        [Documentation]
        ...
        Keyword: check_element
        ...
        ArgSpec(args=['ip', 'port', 'community', 'version'], varargs=None, keywords=None, defaults=(30,))
        [Tags] @author = Sean W
        '''
        return cls.snmp.snmp_next(oid)

    def App_snmp_walk(cls):
        '''
        [Arguments]    ${ip}    ${port}    ${community} =${public}  ${version}
        [Documentation]
        ...
        Keyword: check_element
        ...
        ArgSpec(args=['ip', 'port', 'community', 'version'], varargs=None, keywords=None, defaults=(30,))
        [Tags] @author = Sean W
        '''
        return cls.snmp.snmp_walk()


class App_Web(object):
    def __init__(self):
        pass

    def App_web_login(cls, ip, port, ff):
        '''GUI login
        [Arguments]    ${id}    ${port}'''
        # self.web = WebAppLibrary
        if WebAppLibrary.Web_login(ip, port, ff):
            return True
        else:
            raise 'login failed, please try again!!!'
    
    # @classmethod
    def App_web_logout(cls):
        '''GUI logout'''
        return WebAppLibrary.Web_logout()

    def App_web_find_element_by_id(self, id_):
        '''
        [Arguments]    ${id}
        [Documentation]
        ...
        Keyword: find_element
        ...
        ArgSpec(args=['self', 'id'])
        [Tags] @author = Sean W
        '''
        return WebAppLibrary().Web_find_element_by_id(id_)

    def App_web_find_element_by_id_send(cls, id, key, click):
        '''
        [Arguments]    ${id}    ${key}   ${click}
        [Documentation]
        ...
        Keyword: find_element_send
        ...
        ArgSpec(args=['self', 'id', 'key', 'click'])
        [Tags] @author = Sean W
        '''
        return WebAppLibrary.Web_find_by_id_send(id, key, click)

class App_SSH(object):
    def __init__(self):
        pass

    def ssh_(cls, host, user, password):
        '''login with SSH
        [Arguments]    ${host}'''
        return SshLibrary.ssh_(host, user, password)

    def ssh_session_command_(cls, command='show inter sum'):
        '''write command for SSH
        [Arguments]    ${command}'''
        return  SshLibrary.session_command(command)

    def ssh_reconnection_(cls, host):
        '''reconnection for SSH
        [Arguments]    ${host}'''
        return SshLibrary.reconnection(host)

# App_SSH().ssh_('10.245.46.208')
# App_SSH().session_command('show inter sum')

# aaa = App_Web()
# aaa.App_web_login('10.245.247.60', '3443')
# aaa.App_web_logout()

class App_IXIA(object):
    def __init__(self):
        """
        Connect to the IXIA script server via a socket.
        Connect to the IXIA chassis.
        portList    - must be a list of tuples of three elements: (chassis, card, port)
        srvHost     - name or IP of host running an IXIA Tcl server
        srvPort     - port number the IXIA Tcl server is listening to
        ixiaIp      - IP address of the IXIA chassis
        usrName     - name of IXIA user
        keepOwn     - if True, retain ports ownership even after the script completes
        logProc     - supported values are:
                  o True  - use logging of all ixTclHal commands to stdout (default value)
                  o False - suppress IXIA API command logging
                  o external logging procedure which takes a single argument (a string)
        debugMode   - if True, extended debug output will be performed
        forceOwnership - force ownsership on IXIA ports even somebody else owns them
        """
        pass

    def IXIA_login(self, srvhost, ixiaip, username):
        buffer = ''
        self.srvhost = '10.245.69.200'
        self.svrport = 4555
        self.ixiaip = '10.245.252.54'
        self.username = 'sean'
        self.enter = '\r\n'
        self.sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockobj.connect((self.srvhost, self.svrport))

        command = ['package require IxTclHal ', 'ixConnectToTclServer %s '%self.srvhost, 'ixConnectToChassis %s '%self.ixiaip,
                   'ixGetChassisID %s '%self.ixiaip, 'version cget -productVersion', 'version cget -installVersion',
                   'version cget -ixTclHALVersion']
        self.session_command(command)

        print ("*" * 50)
        for line in open('ixia.txt'):
            self.sockobj.send(line + "\r\n")
            ixiaoutput = self.sockobj.recv(4096).rstrip('\r\n')
            buffer += ixiaoutput
            print (buffer)
        time.sleep(60)
        print ("*" * 50)

    def IXIA_logout(self):
        command = ['ixLogout ', 'ixDisconnectFromChassis %s '%self.ixiaip, 'ixDisconnectTclServer %s '%self.srvhost]
        self.session_command(command)
        self.sockobj.close()

    def session_command(self, command):
        for com in command:
            self.sockobj.send(com + self.enter)
            print (self.sockobj.recv(4096).rstrip(self.enter))