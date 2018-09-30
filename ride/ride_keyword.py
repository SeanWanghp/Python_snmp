# coding=utf-8                                                                  #this must be in first line
#C:\Python27\Doc python
__author__='Maojun'
#data@:2018-08-17
# coding=gbk                                                                    #spell inspection cancelled
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word

#################https://www.cnblogs.com/51kata/p/5126227.html################
'''
regular express for telent into different EQPT
'''
import re as sre
rePrompt                    =  sre.compile('\w+\d+>')
reTL1Prompt                 =  sre.compile('\w+\d+>|\w+\.>')
reShellPrompt               =  sre.compile('\w+:\d+\.\d+:>|\w+\d+:\d+\.\d+:>')
reLinuxPrompt               =  sre.compile('\d+# ')
reC7Prompt                  =  sre.compile('COMPLD|DENY')    #This is for C7 TL1 specically, TL1 command not need 'COMPLD' instead of self.enter
reLoginPrompt               =  sre.compile('\w+\s+login:',    sre.IGNORECASE)
rePasswordPrompt            =  sre.compile('Password:',    sre.IGNORECASE)
reConfirmPrompt             =  sre.compile('y/N',    sre.IGNORECASE)
reAXOSConfirmPrompt         =  sre.compile('~# ',    sre.IGNORECASE)
reAXOSCLIPrompt         =  sre.compile('\.\# ',    sre.IGNORECASE)
reAccuteConfirmPrompt         =  sre.compile('\w+\d+\.>',    sre.IGNORECASE)



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

class MyClass(Singleton):
    '''
    Ride for telent keyword
    '''
    def __init__(self):
        self.tn = self
        self.enter = '\r\n'
        self.timeout = 30
        self.res = tuple
        self.resu = ''
        self.promptList = [rePrompt, reTL1Prompt, reShellPrompt, reLinuxPrompt, reLoginPrompt, rePasswordPrompt,
                           reConfirmPrompt, reC7Prompt, reAXOSConfirmPrompt, reAccuteConfirmPrompt]
 
    def printMsg(self,msg):
        msg = Singleton(SNMP = 'simple network management protocol')
        print "protocol: "+ msg.SNMP

    # def __new__(cls):
    #     print "private telnet running in process"

    def run_cli(self, session, command, prompt=None):
        session.write(str(command) + '\n')
        self.res = session.expect(self.promptList, self.timeout)
        print self.res[2]
        return self.res[2]

    def tl(self, host):
        from telnetlib import Telnet
        self.th = Telnet(host)
        assert isinstance(self.th, object)
        return self.th

    def tel(self, host, port, username, password):
        self.tn = self.tl(host)
        print self.tn.read_until("Username:")
        self.run_cli(self.tn, username)
        self.run_cli(self.tn, password)

    def tel_axos(self, host, port, username, password):
        self.tn = self.tl(host)
        print self.tn.read_until("login: ")
        self.run_cli(self.tn, username)
        self.run_cli(self.tn, password)
        self.run_cli(self.tn, 'cli')
        self.run_cli(self.tn, 'paginate false')
        self.run_cli(self.tn, 'paginate false')
        self.run_cli(self.tn, 'idle-timeout 0')

    def cli(self, cli_command, prompt):
        self.tn.buffer = ''
        print "cli command:", cli_command
        self.tn.output = self.run_cli(self.tn, cli_command)
        self.tn.buffer += self.tn.output
        print self.tn.output

    def __del__(self):
        self.tn.close

    def tel_close(self):
        pass
