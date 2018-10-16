# -*- coding:gbk -*-
'''ʾ��8: װ�����������'''
__author__ = 'Sewang'
#data@:2018-01-17
# coding=gbk                                                                    #spell inspection cancelled
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word
import logging, time, datetime
import functools
import telnetlib

###############class with decorator, parameter transfer###################
'''
��functools���ģ���У���lru_cache���һ�������װ�������ڡ�functools.lru_cache��������Ҫ�����������棬
���ܰ���Ժ�ʱ�ĺ���������б��棬���⴫����ͬ�Ĳ����ظ����㡣ͬʱ�����沢�����������������õĻ���ᱻ�ͷš�
'''


class locker(object):
    '''
    @staticmethod can import without instantiate(ʵ����)
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



class Sean_log:     #ȫ��дLOG�ĺ�������WITH..AS..�̶�����ʵ�֣�װ���д��LOG�ļ��� ���ڻ�д����LOG���˴���BUG���д�FIX����������������
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        self.openedFile = open(self.filename, self.mode)
        # print "*"*20 + "open log file" + "*"*20
        return self.openedFile

    def __exit__(self, *unused):        #������������дLOG�����쳣�����Զ��ر��ļ�
        # print "*"*20 + "finished write log" + "*"*20
        self.openedFile.flush()
        self.openedFile.close()


######################only function with decorator, parameter transfer##############################

def slv_log(**kwargs):  #��һ�������Ӳ�������㺯��������ȥ����ֻ����㣬����û�в�����װ����
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
            with Sean_log(log_path, "a") as writer:    #ʱ����д��%Y_%m_%d&%H_%M_%S
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
def sean_logic(**kwargs):  #��һ�������Ӳ�������㺯��������ȥ����ֻ����㣬����û�в�����װ����
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

    # functools.wraps(func)װ�����������ǽ�func������������Ը��Ƶ�clock��
    # ����˵__name__, __doc__�ȵ�
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