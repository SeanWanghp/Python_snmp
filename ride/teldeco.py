# Date ：2019/11/26 9:19
__author__ = 'Maojun'
import re as sre
import telnetlib
import logging
from functools import wraps
from abc import ABCMeta, abstractmethod
from contextlib import contextmanager


def must_connected(func):
    @wraps(func)
    def wrapper(self, *arg, **kwargs):
        if self.tn:
            self.conne()
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
        try:
            telnetlib.Telnet.__init__(self, host, port if port else 23)
        except EOFError:
            pass
        finally:
            pass

class TelBasic(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def loginto(self):
        print("run in subclass")

    @abstractmethod
    def cli_command(self):
        print("run in subclass")