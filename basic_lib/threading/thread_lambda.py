#-*- encoding: gb2312 -*-
import threading, time
'''
在threading模块中，定义两种类型的锁：threading.Lock和threading.RLock。它们之间有一点细微的区别，通过比较下面两段代码来说明：

import threading
lock = threading.Lock() #Lock对象
lock.acquire()
lock.acquire()  #产生了死锁
lock.release()
lock.release()
import threading
rLock = threading.RLock()  #RLock对象
rLock.acquire()
rLock.acquire() #在同一线程内，程序不会堵塞
rLock.release()
rLock.release()

'''

class Test(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self._run_num = num
    def run(self):
        global count, mutex
        threadname = threading.currentThread().getName()

        for x in xrange(0, int(self._run_num)):
          mutex.acquire()
          count = count + 1
          print threadname, x, count
          mutex.release()

if __name__ == '__main__':
    global count, mutex
    threads = []
    num = 4; count = 1
    # 创建锁
    mutex = threading.Lock()
    # 创建线程对象
    for x in xrange(0, num):
        threads.append(Test(10,))
    # 启动线程
    for t in threads:
        t.start()
        # 等待子线程结束
        t.join()



class MyThread(threading.Thread):
    def __init__(self, condition):
        threading.Thread.__init__(self)
        self.condition = condition

    def run(self):
        global num
        print "%s start"%self.name
        if self.condition == '1':
            if mutex.acquire():
                print "msg: ", self.name + ' set num to ' + str(map(lambda num: num+1, [0, 1]))
                print reduce(lambda a, b: '{};;{}'.format(a, b), [1, 2, 3, 4, 5, 6, 7, 8, 9])
                for i in range(3):
                    print "%s sleep %s seconds"%(self.name, i)
                    # time.sleep(1)

                mutex.release()
        else:
            if mutex.acquire():
                print "msg: ", self.name + ' set num to ' + str(map(lambda num: num-1, [0, 2]))
                for i in range(3):
                    print "%s sleep %s seconds" % (self.name, i)
                    # time.sleep(1)

                mutex.release()
num = 0
mutex = threading.Lock()
def test():
    global mutex
    # for i in range(2):   #every threading will get value from up thread
    t = MyThread('1')
    t1 = MyThread('2')
    t.start()
    t1.start()
    t.join()
    t1.join()

if __name__ == '__main__':
    test()