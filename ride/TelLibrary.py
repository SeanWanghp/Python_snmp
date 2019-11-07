# coding=utf-8                                                                  #this must be in first line
# C:\Python27\Doc python
__author__='Maojun'
# data@:2018-08-17
# coding=gbk                                                                    #spell inspection cancelled
# print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word

#################https://www.cnblogs.com/51kata/p/5126227.html################
'''
regular express for telent into different EQPT
'''
import re as sre
import telnetlib
from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
rePrompt                    =  sre.compile(b'\w+\d+>')
reTL1Prompt                 =  sre.compile(b'\w+\d+>|\w+\.>')
reShellPrompt               =  sre.compile(b'\w+:\d+\.\d+:>|\w+\d+:\d+\.\d+:>')
reLinuxPrompt               =  sre.compile(b'\d+# ')
reC7Prompt                  =  sre.compile(b'COMPLD|DENY')    #This is for C7 TL1 specically, TL1 command not need 'COMPLD' instead of self.enter
reLoginPrompt               =  sre.compile(b'\w+\s+login:',    sre.IGNORECASE)
rePasswordPrompt            =  sre.compile(b'Password:',    sre.IGNORECASE)
reConfirmPrompt             =  sre.compile(b'y/N',    sre.IGNORECASE)
reAXOSConfirmPrompt         =  sre.compile(b'~# ',    sre.IGNORECASE)
reAXOSCLIPrompt         =  sre.compile(b'\.# ',    sre.IGNORECASE)
reAXOSCONFIGPrompt         =  sre.compile(b'\S# ',    sre.IGNORECASE)
reAccuteConfirmPrompt         =  sre.compile(b'\w+\d+\.>',    sre.IGNORECASE)

import logging
# logging.basicConfig函数对日志的输出格式及方式做相关
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

class Tellib(telnetlib.Telnet):
    def __init__(self, host, port):
        try:
            telnetlib.Telnet.__init__(self, host, port if port else 23)
        except EOFError:
            pass
        self.Tel = None
        pass

class TelBasic(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def login(self):
        print("run in subclass")

    @abstractmethod
    def cli_command(self):
        print("run in subclass")


class TelnetLibrary(Singleton):
    '''
    Ride for telent keyword
    '''
    def __init__(self):
        self.tn = None
        self.th = None
        self.enter = b'\r\n'
        self.timeout = 30
        self.res = tuple
        self.resu = b''
        self.promptList = [rePrompt, reTL1Prompt, reShellPrompt, reLinuxPrompt, reLoginPrompt, rePasswordPrompt,
                           reConfirmPrompt, reC7Prompt, reAXOSConfirmPrompt, reAccuteConfirmPrompt, reAXOSCONFIGPrompt]
 
    def printMsg(self,msg):
        msg = Singleton(SNMP = 'simple network management protocol', USERNAME = 'root', PASSWORD = 'root')
        print ("protocol: "+ msg.SNMP)

    # def __new__(cls):
    #     print "private telnet running in process"

    def tl(self, host, port=23):
        self.th = Tellib(host, port)
        assert isinstance(self.th, object)
        return self.th

    def tel(self, host, port, username, password):
        self.tn = self.tl(host)
        print (self.tn.read_until(b"Username: "))
        self.run_cli(self.tn, username.encode('ascii'))
        self.run_cli(self.tn, password.encode('ascii'))

    def tel_axos(self, host, port, username, password):

        self.tn = self.tl(host.encode('ascii'), int(port))
        print (self.tn.read_until(b"login: "))
        command = [username.encode('ascii'), password.encode('ascii'), b'cli', b'cli', b'paginate false', b'show bridge table']
        for com in command:
            self.run_cli(self.tn, com)

    def run_cli(self, session, command, prompt=None):
        session.write(command + b'\n')
        self.res = session.expect(self.promptList, self.timeout)
        print (self.res[2].decode(encoding='utf-8'))
        return self.res[2]

    def cli(self, cli_command, prompt):
        self.tn.buffer = ''
        # print ("cli command:", cli_command)
        self.tn.output = self.run_cli(self.tn, cli_command.encode('ascii'))
        self.tn.buffer += str(self.tn.output)
        # print self.tn.output
        return self.tn.buffer

    def __del__(self):
        # self.th.close()
        pass

    def tel_close(self):
        pass
