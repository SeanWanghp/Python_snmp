# -*- coding:gbk -*-
'''示例8: 装饰器带类参数'''
__author__ = 'Sewang'
#data@:2018-01-17
# coding=gbk                                                                    #spell inspection cancelled
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word
import logging, time, datetime
import functools
import telnetlib

###############class with decorator, parameter transfer###################
'''
在functools这个模块中，有lru_cache这个一个神奇的装饰器存在。functools.lru_cache的作用主要是用来做缓存，
他能把相对耗时的函数结果进行保存，避免传入相同的参数重复计算。同时，缓存并不会无限增长，不用的缓存会被释放。
'''


class locker(object):
    '''
    @staticmethod can import without instantiate(实例化)
    methods, @staticmethod and @classmethod
    '''
    def __init__(self):
        print("locker.__init__() should be not called.")
        self.name = "sean"

    @staticmethod
    def acquire(func):   #func only a parameter of method mirror
        logging.warn("locker.acquire() called.(Start to running %s)" % func.__name__)
        logging.warn("locker.acquire() called.(Start %s)" % func.__doc__)

    @staticmethod
    def release(func):
        logging.warn("locker.release() called.(%s Running finished)" % func.__name__)

    @staticmethod
    def release_finished(func):
        logging.warn("locker.release_finished() called.(%s Running finished)" % func.__name__)


def deco(locker, **kwargs):
    '''
    cls implement acquire and release static method
    '''
    def _deco(func):
        def __deco(*args):
            logging.warn("--%s---- %s called [%s]." % (kwargs, func.__name__, locker))
            locker.acquire(func)   #import function 'acquire'
            try:
                return func(*args)
            finally:
                locker.release(func)    #import function 'release'
                locker.release_finished(func)  # import function 'release_2'
        return __deco
    return _deco

# @deco(locker, h = "haha")
# def myfunc():
#     '''
#     __doc__ running in process
#     :return: None
#     '''
#     print(" myfunc() called.")
#
# myfunc()



class Sean_log:     #全局写LOG的函数，用WITH..AS..固定方法实现，装结果写成LOG文件， 现在会写二遍LOG，此处有BUG，有待FIX。。。。。。。。
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        self.openedFile = open(self.filename, self.mode)
        # print "*"*20 + "open log file" + "*"*20
        return self.openedFile

    def __exit__(self, *unused):        #会输出错误，如果写LOG产生异常，会自动关闭文件
        # print "*"*20 + "finished write log" + "*"*20
        self.openedFile.flush()
        self.openedFile.close()


######################only function with decorator, parameter transfer##############################

def slv_log(**kwargs):  #这一行是增加参数的外层函数，可以去掉，只留里层，就是没有参数的装饰器
    '''
    This deco need function return value
    :param function:
    :return:
    '''
    def deco(func):
        def _deco(*args):
            logging.warn("%s--%s Running with decorator 'slv_log', please waiting!" % (kwargs, func.__name__))
            if func.__doc__:
                logging.warn("%s--%s " % (kwargs, func.__doc__))
            start = time.clock()
            ret = func(*args)

            file_name = "sean_%s.txt"%(datetime.datetime.now().strftime("%Y_%m_%d&%H_h"))
            log_path = "C:\Python27\Doc\E7\SLV384\deco_log\%s"%file_name
            with Sean_log(log_path, "a") as writer:    #时间缩写：%Y_%m_%d&%H_%M_%S
                writer.write(str(ret))

            """
            File copy need after all contents write finished!!!
            """
            import shutil
            backup_log = "C:/Python27/Doc/E7/SLV384/backup_log/%s" % file_name
            shutil.copy(writer.name, backup_log)


            if type(ret) is bool:
                    print logging.warn("%s--%s Running finished.--\n"
                                       "Result is: %s----" % (kwargs, func.__name__, ret))
            elif ret:
                end = time.clock()
                pass
                # logging.warn("%s--%s Running finished.Used time: %ds.\n"
                #              "Result is: %s." % (kwargs, func.__name__, (end - start), ret))

            return ret
        return _deco
    return deco

############################################################################################################
def sean_logic(**kwargs):  #这一行是增加参数的外层函数，可以去掉，只留里层，就是没有参数的装饰器
    def addspam(fn):
        def sayspam(*args):
            print "Telnet in decorator are: ", kwargs, args
            return fn(*args)
        return sayspam
    return addspam


# @addspam
# def useful(a,b):
#     print a**2+b**2
#
# useful(2,3)

##########################################################################################################
a = "10.245.59.210"
b = "wang"

def log_pa(argument):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            print 'before function [%s()] run, text: [%s].' % (function.__name__, argument)
            rst = function(*args, **kwargs)
            print 'after function [%s()] run, text: [%s].' % (function.__name__, argument)
            return rst
        return wrapper
    return decorator

# def func(pa):
#     print 'func() run. %s'%pa
#
# @log_pa(a)
# def turn():
#     func(b)
#     print "running in process"
#
# if '__main__' == __name__:
#     turn()


##########################################################################################################
def addspark(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        print '*.' * 50
        rst = function(*args, **kwargs)
        print '*.' * 50
        return rst
    return wrapper


##########################################################################################################
import time, functools
def clock(func):

    # functools.wraps(func)装饰器的作用是将func函数的相关属性复制到clock中
    # 比如说__name__, __doc__等等
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))
        arg_str = ', '.join(arg_lst)
        print('[%0.8fs] %s(%s) -> %r ' % (elapsed, name, arg_str, result))
        return result
    return clocked