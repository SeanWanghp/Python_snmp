# -*- coding:utf-8 -*-
# C:\Python37\
__author__ = 'Sean Wang'
#data@:2019-10-22
from functools import update_wrapper
import logging
from telnet_ping.config_load.ini_load import *
from telnet_ping.config_load.yaml_load import *
from telnet_ping.config_load.json_load import *


debug = logging.debug
info = logging.info
warn = logging.warning
error = logging.error

yml_data = '''
            student1:
                name: James
                age: 20
            student2:
                name: Lily
                age: 19
            '''


class SingletonClass:
    """Singleton class dec_log
    Use dec_log to restricts the instantiation of a class to one object
    In Caf, we use it is to declare a global object.

    Example:
        @SingletonClass
        class Foo(object): pass
        f1 = Foo()
        f2 = Foo()
        f1 is f2
        True
    """

    def __init__(self, klass):
        self.klass = klass
        self.instance = None
        update_wrapper(self, klass)

    def __call__(self, *args, **kwds):
        if self.instance is None:
            self.instance = self.klass(*args, **kwds)
            # debug code to trace when singleton object is created.
            if not __debug__:
                frameinfo = getframeinfo(currentframe().f_back)
                debug("created singleton instance of %s %s\n" % (str(self.klass), str(self.instance)))
                debug("caller %s:%s:%s\n" % (frameinfo.function, frameinfo.filename, str(frameinfo.lineno)))
                try:
                    frameinfo = getframeinfo(currentframe().f_back.f_back)
                    debug("caller %s:%s:%s\n" % (frameinfo.function, frameinfo.filename, str(frameinfo.lineno)))
                except TypeError:
                    # nothing to do
                    pass

        return self.instance


class Param:
    def __init__(self):
        self.ini_file = None
        self.yml_file = None
        self.json_file = None
        self.ymlhost = self.load_yaml(self.yml_file).load(yml_data)
        self.load_json(self.json_file)

    def load_ini(self, ini_file):
        return Iniset(ini_file)

    def load_yaml(self, yml_file):
        return yml_load(yml_file)

    def load_json(self, json_file):
        return jon_load(json_file)

    def load(self, param_file):
        """following code get from CAFE
        load data file values into Param object
        supported file type are .json, .yaml, .ini
        """
        try:
            file_extension = os.path.splitext(param_file)[-1].lower()
        except:
            file_extension = ""

        # check extension
        if file_extension == ".json":
            self.load_json(param_file)
        elif file_extension == ".ini":
            self.load_ini(param_file)
        elif file_extension == ".yaml":
            self.load_yaml(param_file)
        else:
            raise ParamFileError("unsupported file extension %s. should be one of .json, .yaml, .ini" % file_extension)


class _Config(Param):
    """Singleton class of Caf Config
    In Caf, we use this object to reference to Caf config parameters.\n
    It is subclasss caf.core.utils.Param.\n
    Refer to caf.core.utils.Param for detail usage of this class.\n
    """
    def __int__(self):
        info('Caf Config:\n%s' % pprint.pformat(self))

    def print_config(self):
        info('Caf Config:\n%s' % pprint.pformat(self))

    # def get_time_stamp_path(self, *args):
    #     return self.runner_state.timestamp.path_safe
    #
    # def get_available_log_dir(self, *args):
    #     return self.runner_state.user.available_log_dir
        pass


@SingletonClass
class Config(_Config):
    pass


def get_tel_config():
    """return the Singleton object of Config
    We use Config object to reference the(global) config parameters.
    Returns:
        Config object.

    Examples:
        import telnet_ping
        config = telnet.get_tel_config()
        config.load_xxx(); ##print the config parameters contents

    Note:
        Refer to caf.core.utils.Param for detail usage of Config class. Config is a subclasss of caf.core.utils.Param.
    """
    return Config()


if __name__ == "__main__":
    pass
