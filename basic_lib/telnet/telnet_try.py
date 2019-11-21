# -*- coding:utf-8 -*-
# C:\Python37\
__author__ = 'Maojun'
#data@:2019-10-22
from telnet_ping.telnet_lib import *
import wx
import eyed3
import glob
import logging


class LazyImport:
    """using for dynamic import python libs"""
    def __init__(self, module_name):
        self.module_name = module_name
        self.module = None

    def __getattr__(self, name):
        if self.module is None:
            self.module = __import__(self.module_name)
        return getattr(self.module, name)


tim = LazyImport("time")


class Person(object):
    """using for check parameter value, illegal etc."""
    def __init__(self, age):
        # self.name = name
        self._age = age
        pass

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if 20 < value < 100:
            self._age = value
        else:
            self._age = 23
            logging.warning('port should be 23 in telnet session, invalid age value input!!!')


class E7Telnet(Tellib):
    """init telnetlib"""
    def __init__(self, host, port):
        super(E7Telnet, self).__init__(host, port)
        print("self:", self)
        pass

    def telnet_e7(self, host, port, type=None):
        self.Tel = Tellib(host, port)
        # self.Tel.debuglevel(0)
        res = self.Tel.read_until(b": " or b"# " or b"~ ", 10)
        return self.Tel


class Cli(E7Telnet, TelBasic):
    """main process for telnet and run cli command"""
    def __init__(self, host, port, type, username, password):
        # self.enter = b'\r\n'
        self.res = b''
        self.host = host
        # self.port = port
        self.type = type
        self.username = username
        self.password = password
        self.cli = ''
        self.prompt = ''
        xm = Person(13)     #init property
        xm.age = port    #init property and using age.setter
        self.port = xm.age
        print('age:',  self.port)
        self.session = self.telnet_e7(self.host, self.port, self.type)
        super(Cli, self).__init__(self.host, self.port)
        pass

    def __new__(cls, *args, **kwargs):
        """Give a prompt for user when system running start."""
        logging.warning('AXOS card telnet is checking in process, please waiting...................')
        return object.__new__(cls)   #__init__will not running if no return

    def __call__(self):
        print('telnet is in process')

    def login(self):
        if self.type is 'AXOS':
            self.cli = [self.username, self.password, b"cli"]
            self.prompt = [b": ", b"# ", b"# "]
        elif self.type is 'EXA':
            self.cli = [self.username, self.password, b""]
            self.prompt = [b": ", b"> ", b"> "]
        for cl, pro in zip(self.cli, self.prompt):
            self.session.write(cl + self.enter)
            self.res += self.session.read_until(pro, 5)

    def cli_command(self, command=None):
        for cli in command.split(b'\n'):
            if not cli.strip().startswith(b'#'):
                self.session.write(command.strip() + self.enter)
                self.res += self.session.read_until(b"# ", 5)
                # print([cli_print.decode(encoding='utf-8') for cli_print in self.res.splitlines() if self.res])
                for cli_print in self.res.splitlines():
                    print(cli_print.decode(encoding='utf-8'))
                # tim.sleep(5)
            else:
                print("ignore one command")
        return self.res

    @must_connected
    def run_command(self, cli):
        cli_result = self.cli_command(cli)
        """for dec_log"""
        return cli_result

    def cli_lines(self, image=None):
        """cli_lines using for run cli command"""
        cli = b'''paginate false
                        show card
                        show igmp multicast summary
                        #upgrade activate filename %s'''%image
        return self.run_command(cli)

    def _is_some_method(self):
        return inspect.ismethod(self) or inspect.ismethoddescriptor(self)

    def function_judge(self):
        import inspect
        print(inspect.ismethod(self.run_command))
        print(inspect.isclass(Cli))
        for key, method in inspect.getmembers(E7Telnet, inspect.ismethod):
            '''inspect.getmembers(object[, predicate]) Return all the members of an object in a list of (name, value) 
            pairs sorted by name. If the optional predicate argument is supplied, 
            only members for which the predicate returns a true value are included.'''
            print("key: %s, methond: %s"%(key, method))
            # for item in method:
            #     print "method: ", item
        print(inspect.getmodulename('C:\GitHub\python_lib\telnet_ping\telnet_try.py'))
        print(inspect.getdoc(self.cli_lines))


def run_pro(ip):
    if hasattr(Cli, 'enter') is False:
        getattr(Cli, 'enter', setattr(Cli, 'enter', b'\n'))
        logging.warning('self.enter value init here')
    b = Cli(ip, 13, 'AXOS', username=b'root', password=b'root')
    image = b'http://bamboo.calix.local/artifact/IBAXOS194-CI/shared/build-453/FullRelease.run/' \
            b'FullRelease_system-E7-2_IB-AXOS-19.4_20190924160120_builder.run'
    b.cli_lines(image)
    b.function_judge()


if __name__ == '__main__':
    from multiprocessing import Pool
    ip_pool = ['10.245.46.208', '10.245.46.223', '10.245.46.216', '10.245.46.207']
    p = Pool(processes=len(ip_pool))
    for (ip, times) in zip(ip_pool, range(len(ip_pool))):
        p.apply_async(run_pro, args=(ip,))      #this will running at same time
        # p.apply_async(run_pro(ip,))       #this will cause running step by step
    p.close()
    p.join()
    print("milan" * 100)
