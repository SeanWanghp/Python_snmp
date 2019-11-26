# coding=utf-8
# data@:2018-08-17
# C:\Python27\Doc python
__author__='Maojun'
'''https://www.cnblogs.com/51kata/p/5126227.html
regular express for telent into different EQPT
'''
import re as sre
import telnetlib
import logging
from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
from MaojunLibrary.teldeco import *
rePrompt                    =  sre.compile(b'\w+\d+>')
reTL1Prompt                 =  sre.compile(b'\w+\d+>|\w+\.>')
reShellPrompt               =  sre.compile(b'\w+:\d+\.\d+:>|\w+\d+:\d+\.\d+:>')
reLinuxPrompt               =  sre.compile(b'\d+# ')
"""This is for C7 TL1 specically, TL1 command need 'COMPLD' instead of self.enter"""
reC7Prompt                  =  sre.compile(b'COMPLD|DENY')
reLoginPrompt               =  sre.compile(b'\w+\s+login:',    sre.IGNORECASE)
rePasswordPrompt            =  sre.compile(b'Password:',    sre.IGNORECASE)
reConfirmPrompt             =  sre.compile(b'y/N',    sre.IGNORECASE)
reAXOSConfirmPrompt         =  sre.compile(b'~# ',    sre.IGNORECASE)
reAXOSCLIPrompt         =  sre.compile(b'\.# ',    sre.IGNORECASE)
reAXOSCONFIGPrompt         =  sre.compile(b'\S# ',    sre.IGNORECASE)
reAccuteConfirmPrompt         =  sre.compile(b'\w+\d+\.>',    sre.IGNORECASE)

"""logging.basicConfig函数对日志的输出格式及方式做相关"""
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

class login:
    '''loging parameter'''
    _login_parameter = {}

    def __init__(self):
        self.__dict__ = self._login_parameter

class Singleton(login):  #Inherits from the borg class
    """this class now shares all its attributes among its various instances"""
    #this essenstiaily makes the singleton objects an object-oriented global variable

    def __init__(self, **kwargs):
        login.__init__(self)
        #update the attribute dictionary by inserting a new key-value pair
        self._login_parameter.update(kwargs)

    def __str__(self):
        #return the attribute dictionary for printing
        return str(self._login_parameter)


class TelnetLibrary(Singleton, TelBasic, Tellib):
    '''
    Ride for telent keyword
    '''
    def __init__(self):
        self.tn = None
        self.th = None
        self.enter = b'\n'
        self.timeout = 5
        self.res = tuple
        self.resu = b''
        self.username = None
        self.password = None
        self.type = None
        self.promptList = [rePrompt, reTL1Prompt, reShellPrompt, reLinuxPrompt, reLoginPrompt, rePasswordPrompt,
                           reConfirmPrompt, reC7Prompt, reAXOSConfirmPrompt, reAccuteConfirmPrompt, reAXOSCONFIGPrompt]
 
    def printMsg(self,msg):
        msg = Singleton(SNMP = 'simple network management protocol',
                        USERNAME = 'root', PASSWORD = 'root'
                        )
        print ("protocol: "+ msg.SNMP)

    # def __new__(cls):
    #     print "private telnet running in process"

    def loginto(self, host, username, password, type, port=23):
        self.username = username
        self.password = password
        self.type = type
        self.tn = Tellib(host, int(port))
        print(self.tn.read_until(b': ', 2))
        assert isinstance(self.tn, object)
        return self.tn

    def conne(self):
        self.prompt = []
        self.cl = []
        if self.type in 'axos':
            self.cl = [self.username.encode('ascii'), self.password.encode('ascii'), b"cli"]
            self.prompt = [b"login: ", b"# ", b"# "]
        elif self.type in 'exa':
            self.cl = [self.username.encode('ascii'), self.password.encode('ascii'), b""]
            self.prompt = [b": ", b"> ", b"> "]
        for cc, pro in zip(self.cl, self.prompt):
            self.tn.write(cc + self.enter)
            print(self.tn.read_until(pro, 5))

    def cli_command(self, command, prompt=None):
        self.tn.write(command.encode('ascii') + b'\n')
        self.res = self.tn.expect(self.promptList, self.timeout)
        print (self.res[2].decode(encoding='utf-8'))
        return self.res[2]

    @must_connected
    def cli(self, command, prompt):
        self.tn.buffer = ''
        self.tn.output = self.cli_command(command)
        self.tn.buffer += str(self.tn.output)
        return self.tn.buffer

    def __del__(self):
        # self.th.close()
        pass

    def tel_close(self):
        pass
