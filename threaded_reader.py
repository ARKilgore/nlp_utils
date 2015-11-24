import dependency_structure as dep
from Queue import Queue
from threading import Thread
from multiprocessing.pool import ThreadPool
from time import sleep
import time

pre = '/mnt/corpus/mnt/ainos-research/corpus/nytimes/tree/nyt_'
post = '_sentences.cnlp'


def reader(qin, qout):
    name = qin.get()
    while name != None:

        qout.put(open(name, 'r').readlines())
        name = qin.get()

qout = Queue()
qin = Queue()
ts = []
files = []
for i in range(0, 254):
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

for _ in range(100):
    t = Thread(target=reader, args=(qout, qin))
#    t.daemon = True
    t.start()
    ts.append(t)
    qout.put(None)

for t in ts:
    t.join()

text = []

for _ in range(0, 254):
    text.extend(qin.get())
print 'total time:', str( time.clock() - start )
