

from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
import telnetlib
from time import sleep
from functools import wraps
from try_lib.logging_lib.log import Log


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
        telnetlib.Telnet.__init__(self, host, port if port else 23)
        self.Tel = None
        pass


class TelBasic(object):
    __metaclass__ = ABCMeta

    def __init(self):
        pass

    @abstractmethod
    def login(self):
        print("run in subclass")

    @abstractmethod
    def cli_command(self):
        print("run in subclass")


class Fileopen(object):

    @contextmanager
    def file_open(self, path):
        f_obj = None
        try:
            f_obj = open(path, "w")
            yield f_obj
        except OSError:
            print("We had an error!")
        finally:
            print("Closing file")
            f_obj.close()
