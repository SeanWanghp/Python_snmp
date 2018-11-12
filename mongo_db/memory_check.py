# coding=utf-8                                           #this must be in first line
from E7.SLV384.deco_slv import deco, slv_log
from telnetlib import Telnet
from time import sleep
import logging
# C:\Python27\Doc python
__author__='Sean Wang'
# data@:2018-10-15
# coding=gbk                                             #spell inspection cancelled
# print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word

import re as sre
rePrompt                    =  sre.compile('\w+\d+>')
reTL1Prompt                 =  sre.compile('\w+\d+>|\w+\.>')
reShellPrompt               =  sre.compile('\w+:\d+\.\d+:>|\w+\d+:\d+\.\d+:>')
reLinuxPrompt               =  sre.compile('# ')
reC7Prompt                  =  sre.compile('COMPLD|DENY')    #This is for C7 TL1 specically, TL1 command not need 'COMPLD' instead of self.enter
reLoginPrompt               =  sre.compile('\w+\s+login:',    sre.IGNORECASE)
rePasswordPrompt            =  sre.compile('Password:',    sre.IGNORECASE)
reConfirmPrompt             =  sre.compile('y/N',    sre.IGNORECASE)
reAXOSConfirmPrompt         =  sre.compile('~# ',    sre.IGNORECASE)
reAccuteConfirmPrompt       =  sre.compile('E3VCP>',    sre.IGNORECASE)


class _Log(object):
    '''
    log part for all class
    '''
    def __init__(self):
        pass

    @staticmethod
    def _lg(mess):
        # logging.basicConfig函数对日志的输出格式及方式做相关
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        return logging.warn(mess)


class Para(object):         # property need 'object' for running
    '''
    property with all calsss checking
    # a = Para(5)   # print a.host
    # a.host = 100  # print a.host
    '''
    def __init__(self):
        self._port = None

    def __call__(self, _host):
        self.__dict__ = {'_host': '%s'%_host,
                            '_port': '23',
                            '_type': 'Telnet'}
        return self.__dict__

    def get_port(self):
        return self._port

    def set_port(self, value):
        print "self._port must be 23"
        if not isinstance(value, int):
            raise ValueError('host must be an integer!')
        if value != 23:
            raise ValueError('host must between 23!')
        self._port = value

    def del_port(self):
        del self._port

    port = property(fget=get_port, fset=set_port, fdel=del_port, doc="I'm the property.")

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        if score < 0 or score > 100:
            raise ValueError('invalid score')
        self._score = score
        print 'self._score value is: %s'%self._score
        # return self._score


class e7_telnet(_Log):
    '''
    telnet part for all class
    '''
    def __init__(self):
        # self.Tel = None
        _Log.__init__(self)
        self.function_judge()       #实例化e7_telnet以后不能调用
        pass

    def _getconnection(self, *args, **kwargs):
        """Can be overridden to use a custom connection."""
        if self.telnet_e7(*args, **kwargs):
            pass
        else:
            self._reconnection(*args, **kwargs)
        return self.Tel

    def _reconnection(self, *args, **kwargs):
        # print "session: ", self.session
        if self.session:
            pass
        else:
            print "please check network and wait for 30s to reconnection!!!!"
            sleep(30)
            self.telnet_e7(*args, **kwargs)
        return self.Tel

    def telnet_e7(self, tn, _host, _port, _type=None):
        '''
        Telent to _host and return the session
        '''
        if tn is None:
            self.Tel = Telnet(_host, _port)
            # self.Tel.debuglevel(0)
            self._lg(self.Tel.read_until(": " or "# " or "~ ", 10))
        else:
            pass
        return self.Tel


class _Login(object):
    '''
    login to the server
    '''
    def __init__(self):
        pass

    def login(self):
        if self._type is 'AXOS':
            self.session.write("root" + self.enter)
            self.res += [self.session.read_until(": ")]
            self.session.write("root" + self.enter)
            self.res += [self.session.read_until("# ")]
            self.session.write("pwd" + self.enter)
            self.res += [self.session.read_until("# ")]
            print "res:", self.res
            return self.res
        else:
            raise Exception("equipment type can not find in table")


class _Command(object):
    def __init__(self):
        pass

    def cli_command(self, command):
        '''
        :param command: CLI
        :return: output with the command
        '''
        for cli in command.split('\n'):
            if not cli.strip().startswith('#'):
                self.session.write(command.strip() + self.enter)
                self.res = self.session.expect(['# ', '~#'])
                # print self.res[2]
                self.resu += self.res[2]
            else:
                print "ignore one command"
        return self.resu

    def step_command(self, command, prompt=None):
        '''
        :param command:
        :param prompt:
        :return: output from the command
        '''
        self.session.write(command + self.enter)
        return self.session.read_until(prompt)

class _Mongogo(object):
    '''
    mongo database running
    '''
    def __init__(self):
        pass

    # @staticmethod
    def mongo_write(self, memory_dict=None, action=None, memory_filter=None, card_ip=None):
        import pymongo
        '''
        http://www.runoob.com/python3/python-mongodb.html   MONGDB操作方法网址
        '''
        self._x = []
        self._y = []
        plt_status = ['static', 'dynamic']
        self.plt_st = plt_status[0]
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        user = myclient["maojun"]
        dbname = user["sean"]

        if action == 'add' and memory_filter == None:
            dbname.insert_one(memory_dict)

        elif action == 'print' and memory_filter != None:
            for x in dbname.find({"module_name": "%s" % memory_filter}):
                for key, value in x.items():
                    # print "key is: %s, value is: %s" % (key, value)
                    if key == 'CUP':
                        self._x.append(value)
                    elif key == 'Memory':
                        self._y.append(value)

            if self.plt_st == 'static':
                plt = self.static_plt(self._x, self._y, memory_filter, card_ip)
                return plt
            if self.plt_st == 'dynamic':
                plt = self.dynamic_plt(self._x, self._y, memory_filter, card_ip)
                return plt

        elif action == None and memory_filter != None:
            myquery = {"module_name": "%s"%memory_filter}
            for x in dbname.find(myquery).sort([['_id', 1]]):
                print "\033[0;31m%s\033[0m"%x
        else:
            return None

class _Matlibplt(object):
    '''
    matlib running
    '''
    def __init__(self):
        pass

    def static_plt(self, x, y, memory_filter, card_ip):
        '''
        画图参考： https://www.cnblogs.com/zhizhan/p/5615947.html
        颜色参考： https://www.cnblogs.com/darkknightzh/p/6117528.html
        plt.legend with loc value as following:
        right, center left, upper right, lower right, best, center
        lower left, center right, upper left, upper center, lower center
        '''
        import matplotlib.pyplot as plt
        print "CPU: {}".format(x)
        print "MEMORY: {}".format(y)
        self.cpu_co = ''
        self.mem_co = ''
        if memory_filter == self.module_a:
            self.cpu_co = '-r'
            self.mem_co = '-g'
        elif memory_filter == self.module_b:
            self.cpu_co = '-m'
            self.mem_co = '-b'
        plt.plot(x, self.cpu_co, label='%s CPU'%memory_filter)
        plt.plot(y, self.mem_co, label='%s MEMORY'%memory_filter)

        plt.legend(loc= 'center right')
        plt.xlabel('time')
        plt.ylabel('CPU&MEMORY')
        plt.title('%s cpu&memory'%(card_ip))
        return plt

    @staticmethod
    def dynamic_plt(x, y, memory_filter, card_ip):
        import matplotlib.pyplot as plt
        import numpy as np
        '''
        Reference:   C:\Python27\Doc\basic_lib\matlib_basic\dynamic_matlib.py
        '''
        fig, ax = plt.subplots()
        # fig2, ax2=plt.subplots()
        y1 = []
        y2 = []
        for i,j in zip(x, y):
            y1.append(i)
            y2.append(j)
            plt.cla()
            plt.title('%s cpu&memory'%(card_ip))
            plt.xlabel("Time")
            plt.ylabel("CPU&MEMORY")
            plt.xlim(0, len(x))
            plt.ylim(0, 50)
            plt.grid()
            plt.plot(y1, label='%s CPU'%memory_filter)
            plt.plot(y2, label='%s MEMORY'%memory_filter)
            plt.legend(loc='upper right')
            # plt.draw()
            plt.pause(0.001)
        return plt

class _Cli(e7_telnet, Para, _Log, _Login, _Command, _Mongogo, _Matlibplt):
    def __init__(self, _host, _port, _type):
        super(_Cli, self).__init__()
        self.promptList = [rePrompt, reTL1Prompt, reShellPrompt, reLinuxPrompt, reLoginPrompt, rePasswordPrompt,
                           reConfirmPrompt, reC7Prompt, reAXOSConfirmPrompt, reAccuteConfirmPrompt]
        # self.enter = '\r\n'
        self.score = 10
        self._host = _host
        print "self: ", self('%s' % self._host)     #__call__ will showing up
        self.port = _port               # Para().port = _port   #import property class to check parameter
        self._port = Para().port
        self._type = _type
        self.session = None
        self.res = []
        self.resu = ''
        self.session = self.tel_init(self, self.session, self._host, self._port, self._type)
        self._get_login()

    def __new__(cls, *args, **kwargs):
        '''
        Give a prompt for user when system running start.
        '''
        logging.warn('AXOS card CPU&MEMORY is checking in process, please waiting...................')
        return object.__new__(cls)   #__init__will not running if no return

    def __del__(self):
        '''
        close the session
        '''
        self.session.write('exit' + self.enter)
        try:
            self.session.close()
            return self._lg("telnet session closed!")
            # print "session closed"
        except BaseException, e:
            print e.message

    @classmethod
    def tel_init(cls, tel, tn, host, port, _type):
        """Can be overridden telnet connection"""
        sess = tel._getconnection(tn, host, port, _type)
        return sess

    def _get_login(self, *args):
        """Can be overridden login."""
        return self.login(*args)

    def ftp_get_baseline(self, ftp_ip, ftp_user, ftp_password, baseline_version):
        '''
        using ftp server to get the baseline
        '''
        self.step_command('ftp %s'%ftp_ip, ": ")
        self.step_command('%s'%ftp_user, ":")
        self.step_command('%s'%ftp_password, "> ")
        self.step_command('ls', "> ")
        self.step_command('get %s'%baseline_version, "> ")
        self.step_command('bye', "# ")

    @slv_log(name='maojun')
    def memory_check_run(self, module_a, module_b, card_ip):
        '''
        check axos memory in process
        '''
        print "memory checking"
        self.module_a = module_a
        self.module_b = module_b
        self.memory_dict = {}
        self.memory_update = {}
        self.id_number = int
        self.plt = None
        import random
        self.cli_command('cd /var/log/mem_check')
        # self.cli_command('cat lmd.log')
        # self.cli_command('cat /var/log/mem_check_results.log ')
        all_memory = self.cli_command('ps aux --sort -rss')
        with open('memory.txt', 'w+') as f:
            f.write(all_memory)
        module_re = sre.compile("\s+\/\w+\/\w+\/(\w+)")
        memory_re = sre.compile("root\s+\d+\s+(\d+.\d+)\s+(\d+.\d+)")
        for line_memory in all_memory.splitlines():
            # print line_memory
            self.id_number = random.randint(1, 1000000000000000)
            memory_content = memory_re.match(line_memory)
            if memory_content:
                if memory_content.group(1) != '0.0' and float(memory_content.group(2)) >= 5:
                    module_name = module_re.search(line_memory)
                    if module_name:
                        print "module_name: \033[0;31m%s\033[0m"%module_name.group(1)
                        self.memory_dict['module_name'] = module_name.group(1)
                    else:
                        print "module name not matched"
                    print "CPU: \033[0;31m%s\033[0m" % memory_content.group(1)
                    print "Memory: \033[0;31m%s\033[0m" % memory_content.group(2)
                    self.memory_dict['CUP'] = memory_content.group(1)
                    self.memory_dict['Memory'] = memory_content.group(2)
                    self.memory_dict['_id'] = self.id_number
                    self.mongo_write(self.memory_dict, 'add')
                else:
                    continue
            else:
                continue

        print "memory_dict: {}".format(self.memory_dict)
        import threading
        module_lib = [module_a, module_b]
        for module_run in module_lib:
            self.plt = self.mongo_write(None, 'print', module_run, card_ip)
        self.plt.show()
        # print self.cli_command('par -a leak -0 ')
        # print self.cli_command('par -a mem -0 ')
        # print self.cli_command('par -a cpu -0 ')
        return all_memory


    def cli_lines(self, module_a, module_b, card_ip):
        '''
        cli_lines using for run cli command
        '''
        print card_ip
        return self.memory_check_run(module_a, module_b, card_ip)

    def function_judge(self):
        '''
        # inspect.getmembers(object[, predicate]) Return all the members of an object in a list of (name, value) pairs sorted by name.
        If the optional predicate argument is supplied, only members for which the predicate returns a true value are included.
        :return:
        '''
        import inspect
        print "inspect process starting ---------------------------------"
        print inspect.ismethod(self.memory_check_run)
        print inspect.isclass(_Cli)
        for key, method in inspect.getmembers(e7_telnet, inspect.ismethod):
            print "key: %s, methond: %s"%(key, method)
            # for item in method:
            #     print "method: ", item
        print inspect.getmodulename('C:\\Python27\\Doc\\telnet_ping\\telnet_try.py')
        print inspect.getdoc(self.cli_lines)
        print "inspect process stopped ---------------------------------"


if __name__ == "__main__":
    if hasattr(_Cli, 'enter') is False:
        getattr(_Cli, 'enter', setattr(_Cli, 'enter', '\n'))
        # sleep(600)
    card_ip = '10.245.46.215'
    module_a = 'lmd'
    module_b = 'halm'
    b = _Cli(card_ip, 23, 'AXOS')
    print "_cli 属性有哪些：{}".format(b.__dict__)
    b.cli_lines(module_a, module_b, card_ip)