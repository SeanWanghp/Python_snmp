

#!/usr/bin/env python
# -*- coding: utf-8 -*-


import threading
import time
import random

semaphore = threading.Semaphore(0)

def consumer():
    print("consumer is waiting.")
    semaphore.acquire()
    print("Consumer notify: consumed item number %s." % item)

def producer():
    global item
    print("sleep one second.")
    time.sleep(1)
    item = random.randint(1, 1000)
    print("producer nofity: produced item number %s." % item)
    semaphore.release()


if __name__ == "__main__":

    for i in range(0, 5):
        t1 = threading.Thread(target=producer)
        t2 = threading.Thread(target=consumer)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    print("program teminated.")