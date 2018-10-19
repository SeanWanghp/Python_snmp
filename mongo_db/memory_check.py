# coding=utf-8                                           #this must be in first line
#C:\Python27\Doc python
__author__='Sean Wang'
#data@:2018-10-15
# coding=gbk                                             #spell inspection cancelled
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word


from E7.SLV384.deco_slv import deco
from telnetlib import Telnet
from time import sleep
import logging
# logging.basicConfig函数对日志的输出格式及方式做相关
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

class Para(object):         #property need 'object' for running
    '''
    # a = Para(5)
    # print a.host
    # a.host = 100
    # print a.host
    '''
    def __init__(self):
        self._port = None

    def get_port(self):
        return self._port

    def set_port(self, value):
        print "_port is 23"
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


class e7_telnet(object):
    def __init__(self):
        print "self:", self()
        self.function_judge()
        pass

    def __call__(self):
        self.__dict__ = {'_host': 'x.x.x.x',
                            '_port': '23',
                            '_type': 'ssh'}
        return self.__dict__


    def telnet_e7(self, _host, _port, _type=None):
        '''
        Telent to _host and return the session
        '''
        self.Tel = Telnet(_host, _port)
        # self.Tel.debuglevel(0)
        res = self.Tel.read_until(": " or "# " or "~ ")
        return self.Tel


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
reAccuteConfirmPrompt         =  sre.compile('E3VCP>',    sre.IGNORECASE)

class cli(e7_telnet, Para):
    def __init__(self, _host, _port, _type):
        super(cli, self).__init__()

        # self.enter = '\r\n'
        self.res = ''
        self._host = _host
        Para().port = _port         #import property class to check parameter
        self._port = Para().port
        self._type = _type
        self.session = self.telnet_e7(self._host, self._port, self._type)
        self.score = 10
        print self.score
        self.login()
        self.promptList = [rePrompt, reTL1Prompt, reShellPrompt, reLinuxPrompt, reLoginPrompt, rePasswordPrompt,
                           reConfirmPrompt, reC7Prompt, reAXOSConfirmPrompt, reAccuteConfirmPrompt]

    def __new__(cls, *args, **kwargs):
        '''
        Give a prompt for user when system running start.
        '''
        logging.warn('SMX server2 upgrade in process, please waiting...................')
        return object.__new__(cls, *args, **kwargs)   #__init__will not running if no return

    def __del__(self):
        '''
        close the session
        '''
        self.session.write('exit' + self.enter)
        try:
            self.session.close()
            logging.warn("telnet session closed!")
        except BaseException, e:
            print e.message

    def login(self):
        '''
        login to the server
        '''
        if self._type == None:
            self.session.write("root" + self.enter)
            self.res += self.session.read_until(": ")
            self.session.write("root" + self.enter)
            self.res += self.session.read_until("# ")
            self.session.write("pwd" + self.enter)
            self.res += self.session.read_until("# ")

    def cli_command(self, command):
        '''
        :param command: CLI
        :return: output with the command
        '''
        self.resu = ''
        for cli in command.split('\n'):
            if not cli.strip().startswith('#'):
                self.session.write(command.strip() + self.enter)
                self.res = self.session.expect(['# ', '~#'])
                # print self.res[2]
                self.resu += self.res[2]
            else:
                print "ignore one command"
        return self.resu

    def step_command(self, command, prompt):
        '''
        :param command:
        :param prompt:
        :return: output from the command
        '''
        self.session.write(command + self.enter)
        print self.session.read_until(prompt)


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

    @deco(name= 'maojun')
    def run_command(self, cli, card_ip):
        '''
        upgrade SMx server detail process
        '''
        self.memory_dict = {}
        self.memory_update = {}
        import random
        self.cli_command('cd /var/log/mem_check')
        self.cli_command('cat lmd.log')
        self.cli_command('cat /var/log/mem_check_results.log ')
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
                print "no match part found"

        print "memory_dict: ", self.memory_dict
        self.mongo_write(None, 'print', 'lmd', card_ip)
        self.mongo_write(None, 'print', 'halm', card_ip)
        # print self.cli_command('par -a leak -0 ')
        # print self.cli_command('par -a mem -0 ')
        # print self.cli_command('par -a cpu -0 ')

    # @staticmethod
    def mongo_write(self, memory_dict=None, action=None, memory_filter=None, card_ip=None):
        import pymongo
        '''
        http://www.runoob.com/python3/python-mongodb.html   MONGDB操作方法网址
        '''
        self._x = []
        self._y = []
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

            self.mat_plt(self._x, self._y, memory_filter, card_ip)

        elif action == None and memory_filter != None:
            myquery = {"module_name": "%s"%memory_filter}
            for x in dbname.find(myquery).sort([['_id', 1]]):
                print "\033[0;31m%s\033[0m"%x
        else:
            return None

    def mat_plt(self, x, y, memory_filter, card_ip):
        '''
        plt.legend with loc value as following:
        right
        center left
        upper right
        lower right
        best
        center
        lower left
        center right
        upper left
        upper center
        lower center
        '''
        import matplotlib.pyplot as plt
        print "CPU: ", x
        print "MEMORY: ", y
        plt.plot(x, '-r', label = 'CPU')
        plt.plot(y, '-g', label = 'MEMORY')

        plt.legend(loc = 'center right')

        plt.xlabel('time')
        plt.ylabel('CPU&MEMORY')
        # plt.text(2, 10, r'CPU, MEMORY')
        plt.title('%s %s cpu&memory'%(card_ip, memory_filter))
        plt.show()

    def cli_lines(self, card_ip):
        '''
        cli_lines using for run cli command
        '''
        cli = '''ls'''
        print card_ip
        return self.run_command(cli, card_ip)

    def function_judge(self):
        '''
        # inspect.getmembers(object[, predicate]) Return all the members of an object in a list of (name, value) pairs sorted by name.
        If the optional predicate argument is supplied, only members for which the predicate returns a true value are included.
        :return:
        '''
        import inspect
        print "inspect process starting ---------------------------------"
        print inspect.ismethod(self.run_command)
        print inspect.isclass(cli)
        for key, method in inspect.getmembers(e7_telnet, inspect.ismethod):
            print "key: %s, methond: %s"%(key, method)
            # for item in method:
            #     print "method: ", item
        print inspect.getmodulename('C:\\Python27\\Doc\\telnet_ping\\telnet_try.py')
        print inspect.getdoc(self.cli_lines)
        print "inspect process stopped ---------------------------------"


if __name__ == "__main__":
    getattr(cli, 'enter', setattr(cli, 'enter', '\n'))
    # sleep(600)
    card_ip = '10.245.46.215'
    b = cli(card_ip, 23, None)
    b.cli_lines(card_ip)


