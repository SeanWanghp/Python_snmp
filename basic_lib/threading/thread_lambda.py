#-*- encoding: gb2312 -*-
import threading, time
from functools import reduce
'''
��threadingģ���У������������͵�����threading.Lock��threading.RLock������֮����һ��ϸ΢������ͨ���Ƚ��������δ�����˵����

import threading
lock = threading.Lock() #Lock����
lock.acquire()
lock.acquire()  #����������
lock.release()
lock.release()
import threading
rLock = threading.RLock()  #RLock����
rLock.acquire()
rLock.acquire() #��ͬһ�߳��ڣ����򲻻����
rLock.release()
rLock.release()

https://www.cnblogs.com/nanqiang/p/9910860.html
ͬ�����첽�������������������
1����������
���źܶ����linux��̨���������Ķ��Ӵ���ͬ��&�첽������&�����������ĸ��Ҳ���Ŷ�������������⣬������Ϊͬ�������������첽���Ƿ������������������������⼸������ֱ���ʲô���塣
ͬ����
��νͬ���������ڷ���һ�����ܵ���ʱ����û�еõ����֮ǰ���õ��þͲ����ء�Ҳ���Ǳ���һ��һ������,��ǰһ�������˲�������һ���¡�
������ͨB/Sģʽ��ͬ�������ύ����->�ȴ�����������->������Ϸ��� ����ڼ�ͻ�����������ܸ��κ���
�첽��
�첽�ĸ����ͬ����ԡ���һ���첽���̵��÷����󣬵����߲������̵õ������ʵ�ʴ���������õĲ�������ɺ�ͨ��״̬��֪ͨ�ͻص���֪ͨ�����ߡ�
���� ajax�����첽��: ����ͨ���¼�����->���������������������Ȼ�������������飩->�������
������
����������ָ���ý������֮ǰ����ǰ�̻߳ᱻ�����߳̽���ǿ�ִ��״̬�������״̬�£�cpu������̷߳���ʱ��Ƭ�����߳���ͣ���У�������ֻ���ڵõ����֮��Ż᷵�ء�
����Ҳ�����������ú�ͬ�����õ�ͬ������ʵ�������ǲ�ͬ�ġ�����ͬ��������˵���ܶ�ʱ��ǰ�̻߳��Ǽ���ģ�ֻ�Ǵ��߼��ϵ�ǰ����û�з���,��������ռcpuȥִ�������߼���Ҳ���������io�Ƿ�׼���á�
������
�������������ĸ������Ӧ��ָ�ڲ������̵õ����֮ǰ���ú�������������ǰ�̣߳��������̷��ء�

�ټ򵥵������ǣ�
1. ͬ���������ҵ���һ�����ܣ��ù���û�н���ǰ�������Ƚ����
2. �첽�������ҵ���һ�����ܣ�����Ҫ֪���ù��ܽ�����ù����н����֪ͨ�ң��ص�֪ͨ��
3. ���������ǵ����ң����������ң�������û�н��������ݻ���û�еõ����֮ǰ���Ҳ��᷵�ء�
4. �����������ǵ����ң����������ң��������������أ�ͨ��select֪ͨ������

ͬ��IO���첽IO����������ڣ����ݿ�����ʱ������Ƿ�����
����IO�ͷ�����IO����������ڣ�Ӧ�ó���ĵ����Ƿ���������
���Ͽ�֪��ͬ�����첽,�����ͷ�����,��Щ����,��ʵ������ȫ����һ����,�����������εĶ���Ҳ����ͬ��

2������IOģ��
���˽���ͬ�����첽����������������������������linux������IOģ�ͣ�
1)����I/O��blocking I/O��
2)������I/O ��nonblocking I/O��
3) I/O����(select ��poll) ��I/O multiplexing��
4)�ź�����I/O ��signal driven I/O (SIGIO)��
5)�첽I/O ��asynchronous I/O (the POSIX aio_functions)��
����ǰ4�ֶ���ͬ�������һ�ֲ����첽��
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
