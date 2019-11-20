#-*- encoding: gb2312 -*-
import threading, time
from functools import reduce
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

https://www.cnblogs.com/nanqiang/p/9910860.html
同步与异步，阻塞与非阻塞的区别
1、概念剖析
相信很多从事linux后台开发工作的都接触过同步&异步、阻塞&非阻塞这样的概念，也相信都曾经产生过误解，比如认为同步就是阻塞、异步就是非阻塞，下面我们先剖析下这几个概念分别是什么含义。
同步：
所谓同步，就是在发出一个功能调用时，在没有得到结果之前，该调用就不返回。也就是必须一件一件事做,等前一件做完了才能做下一件事。
例如普通B/S模式（同步）：提交请求->等待服务器处理->处理完毕返回 这个期间客户端浏览器不能干任何事
异步：
异步的概念和同步相对。当一个异步过程调用发出后，调用者不能立刻得到结果。实际处理这个调用的部件在完成后，通过状态、通知和回调来通知调用者。
例如 ajax请求（异步）: 请求通过事件触发->服务器处理（这是浏览器仍然可以作其他事情）->处理完毕
阻塞：
阻塞调用是指调用结果返回之前，当前线程会被挂起（线程进入非可执行状态，在这个状态下，cpu不会给线程分配时间片，即线程暂停运行）。函数只有在得到结果之后才会返回。
有人也许会把阻塞调用和同步调用等同起来，实际上他是不同的。对于同步调用来说，很多时候当前线程还是激活的，只是从逻辑上当前函数没有返回,它还会抢占cpu去执行其他逻辑，也会主动检测io是否准备好。
非阻塞
非阻塞和阻塞的概念相对应，指在不能立刻得到结果之前，该函数不会阻塞当前线程，而会立刻返回。

再简单点理解就是：
1. 同步，就是我调用一个功能，该功能没有结束前，我死等结果。
2. 异步，就是我调用一个功能，不需要知道该功能结果，该功能有结果后通知我（回调通知）
3. 阻塞，就是调用我（函数），我（函数）没有接收完数据或者没有得到结果之前，我不会返回。
4. 非阻塞，就是调用我（函数），我（函数）立即返回，通过select通知调用者

同步IO和异步IO的区别就在于：数据拷贝的时候进程是否阻塞
阻塞IO和非阻塞IO的区别就在于：应用程序的调用是否立即返回
综上可知，同步和异步,阻塞和非阻塞,有些混用,其实它们完全不是一回事,而且它们修饰的对象也不相同。

2、五种IO模型
在了解了同步与异步、阻塞与非阻塞概念后，我们来讲讲linux的五种IO模型：
1)阻塞I/O（blocking I/O）
2)非阻塞I/O （nonblocking I/O）
3) I/O复用(select 和poll) （I/O multiplexing）
4)信号驱动I/O （signal driven I/O (SIGIO)）
5)异步I/O （asynchronous I/O (the POSIX aio_functions)）
其中前4种都是同步，最后一种才是异步。
'''


class Test(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self._num = num
        self.count = 1
        self.mutex = threading.Lock()

    def run(self):
        threadname = threading.currentThread().getName()
        for x in range(0, int(self._num)):
            self.mutex.acquire()
            count = self.count + 1
            print(threadname, x, count)
            self.mutex.release()


if __name__ == '__main__':
    """all theads will running at same time"""
    th = None
    threads = []
    num = 2
    for x in range(0, num):
        threads.append(Test(5,))
    for th in threads:
        th.start()
    th.join()


class MyThread(threading.Thread):
    def __init__(self, condition):
        threading.Thread.__init__(self)
        self.condition = condition
        num = 0
        self.mutex = threading.Lock()

    def run(self):
        global num
        print("%s start" % self.name)
        if self.condition == '1':
            if self.mutex.acquire():
                print("msg: ", self.name + ' set num to ' + str(map(lambda num: num+1, [0, 1])))
                print(reduce(lambda a, b: '{};;{}'.format(a, b), [1, 2, 3, 4, 5, 6, 7, 8, 9]))
                for i in range(3):
                    print("%s sleep %s seconds"%(self.name, i))
                    # time.sleep(1)

                self.mutex.release()
        else:
            if self.mutex.acquire():
                print("msg: ", self.name + ' set num to ' + str(map(lambda num: num-1, [0, 2])))
                for i in range(3):
                    print("%s sleep %s seconds" % (self.name, i))
                    # time.sleep(1)

                self.mutex.release()


def test():
    t = None
    t1 = None
    for i in range(1):   #every threading will get value from up thread
        t = MyThread('1')
        t1 = MyThread('2')
        t.start()
        t1.start()
    t.join()
    t1.join()


if __name__ == '__main__':
    test()
