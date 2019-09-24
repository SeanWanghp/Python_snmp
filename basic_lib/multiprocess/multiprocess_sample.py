# coding=utf-8
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from multiprocessing import Pool
import os, time, random, multiprocessing


def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))


if __name__ == '__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.\n')


class Producer(multiprocessing.Process):
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue

    def run(self):
        for i in range(5):
            item = random.randint(0,256)
            self.queue.put(item)
            print("process producer: item %d appended to queue %s"%(item, self.name))
            # time.sleep(1)
            print("the size of queue is %s"% self.queue.qsize())


class Consumer(multiprocessing.Process):
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue

    def run(self):
        try:
            if self.queue.empty():
                print("the queue is empty")
            else:
                item = self.queue.get(block=True, timeout=2)
                print('process consumer: item %d popped from by %s \n'%(item, self.name))
                # time.sleep(1)
        except e:
            print(e)


class Apple(Consumer):
    def __init__(self, times):
        super(Apple, self).__init__(times)
        self.times = times

    def run(self):
        for i in range(self.times):
            item = random.randint(0, 256)
            print("process apple: item %d appended to queue %s"%(item, self.name))
            print("the size of queue is %s"% i)


if __name__ == "__main__":
    queue = multiprocessing.Queue()
    process_producer = Producer(queue)
    process_consumer = Consumer(queue)
    process_apple = Apple(3)
    process_run = [process_producer, process_consumer, process_apple]
    for run in process_run:
        run.start()
        run.join()

