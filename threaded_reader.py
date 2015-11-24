import dependency_structure as dep
from Queue import Queue
from threading import Thread
from multiprocessing.pool import ThreadPool
from time import sleep
import time

pre = '/mnt/mnt/ainos-research/corpus/nytimes/tree/nyt_'
post = '_sentences.cnlp'


def reader(qin, qout):
    name = qin.get()
    while name != None:
        print 'parsing', name
        qout.put(open(name, 'r').readlines())
        print 'parsed', name
        name = qin.get()
    print 'dead'

def t_read(threads=100, upper=254):
    qout = Queue()
    qin = Queue()
    ts = []
    files = []
    for i in range(0, upper):
        if i < 10:
            i = '00' + str(i)
        elif i < 100:
            i = '0' + str(i)
        else:
            i = str(i)
        files.append(pre+i+post)
    for f in files:
        qout.put(f)
    start = time.clock()

    for _ in range(min(threads, upper)):
        t = Thread(target=reader, args=(qout, qin))
#    t.daemon = True
        t.start()
        ts.append(t)
        qout.put(None)

    for t in ts:
        t.join()

    text = []

    for _ in range(0, upper):
        text.extend(qin.get())
        print 'got text'
    print 'total time:', str( time.clock() - start )
    return text
