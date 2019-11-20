# coding=utf-8
#C:\Python27\Doc python
__author__ = 'Maojun Wang'
#data@:2018-10-10
# coding=utf-8
import threading
import time

con = threading.Condition()
num = 0


class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global num
        con.acquire()
        while True:
            print("开始添加！！！")
            num += 1
            print("火锅里面鱼丸个数：%s" % str(num))
            time.sleep(1)
            if num >= 5:
                print("火锅里面里面鱼丸数量已经到达5个，无法添加了！")
                """wake up waited thread"""
                con.notify()
                """wait for notify"""
                con.wait()
            con.release()


class Consumers(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        con.acquire()
        global num
        while True:
            print("开始吃啦！！！")
            num -= 1
            print("火锅里面剩余鱼丸数量：%s" % str(num))
            time.sleep(2)
            if num <= 0:
                print("锅底没货了，赶紧加鱼丸吧！")
                """wake up other thread"""
                con.notify()
                """wait for notify"""
                con.wait()
            con.release()


pp = Producer()
cc = Consumers()
pp.start()
cc.start()