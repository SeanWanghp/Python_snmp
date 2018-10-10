# coding=utf-8
#C:\Python27\Doc python
__author__='Maojun Wang'
#data@:2018-10-10
import threading, time

class MyThread(threading.Thread):
    def __init__(self, signal):
        threading.Thread.__init__(self)
        # 初始化
        self.singal = signal

    def run(self):
        print "I am %s,I will sleep ..."% self.name
        # 进入等待状态
        self.singal.wait()
        print "I am %s, I awake..." % self.name


if __name__ == "__main__":
    # 初始 为 False
    singal = threading.Event()
    for t in range(0, 3):
        thread = MyThread(singal)
        thread.start()

    print "main thread sleep 3 seconds... "
    time.sleep(3)
    # 　唤醒含有signal,　处于等待状态的线程
    singal.set()



# def do(event):
#     print 'start'
#     event.wait()
#     print 'execute'
#
#
# event_obj = threading.Event()
# for i in range(10):
#     t = threading.Thread(target=do, args=(event_obj,))
#     t.start()
#
# event_obj.clear() #继续阻塞
# inp = raw_input('input:')
# if inp == 'true':
#     event_obj.set()  # 唤醒