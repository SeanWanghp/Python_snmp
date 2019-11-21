
# -*- coding:utf-8 -*-
# C:\Python37\
__author__ = 'Sean Wang'
#data@:2019-10-22
#update data@:2019-xx-xx                  #spell inspection cancelled
from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
import telnetlib
from time import sleep
from functools import wraps
from try_lib.logging_lib.log import Log
import telnet_ping


class Singleton:
    __instance = None

    def __init__(self):
        print("我是init方法.")

    def __new__(cls):
        if not Singleton.__instance:
            Singleton.__instance = object.__new__(cls)
        return Singleton.__instance


def must_connected(func):
    @wraps(func)
    def wrapper(self, *arg, **kwargs):
        if self.session:
            self.login()
        return func(self, *arg, **kwargs)
    return wrapper


def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            Log.warning('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator


class Tellib(telnetlib.Telnet):
    def __init__(self, host, port):
        # telnetlib.Telnet.__init__(self, host, port)
        super(Tellib, self).__init__(host, port, timeout=10)
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


class ConfigError(Exception): pass
'''following code from CAFE'''


class Telconfig:
    def __init__(self):
        self.telyml = {}
        pass

    @property
    def config(self):
        # telnet_ping.Iniset()
        print('ymlhost: ', telnet_ping.get_tel_config().ymlhost)
        return telnet_ping.get_tel_config()

    @config.setter
    def config(self, value):
        if isinstance(value, list):
            telnet_ping.get_tel_config().ymlhost = value
        else:
            ConfigError("error:list is must")

    def check_config_ini(self, inifile):
        self.config.load_ini(ini_file=inifile)      #can using 'self.config' when property set up parameter


class Checkconfig(Telconfig):

    def __init__(self):
        super(Checkconfig, self).__init__()
        print(self.check_config_ini('mysql.ini'))


print('check_config: ', Checkconfig())


class Fileopen(object):

    @contextmanager
    def file_open(self, path):
        f_obj = None
        # with open(path, 'w') as f_obj:
        #     yield f_obj
        #     print("close file ......")
        #     f_obj.close()
        try:
            f_obj = open(path, "w")
            yield f_obj
        except OSError:
            print("We had an error!")
        finally:
            print("Closing file.....")
            f_obj.close()


if __name__ == "__main__":
    with Fileopen().file_open("contextmanager.txt") as fobj:
        fobj.write("Testing context managers")
        for i in range(1, 3):
            print(i)
