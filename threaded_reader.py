import dependency_structure as dep
import glob
from Queue import Queue
from threading import Thread
from multiprocessing.pool import ThreadPool
from time import sleep
import time

prenyt = '/data/mnt/ainos-research/corpus/nytimes/tree/*.cnlp'
prewiki = '/data/mnt/ainos-research/corpus/wikipedia2015/tree/*.cnlp'


def reader(qin, qout, is_build_vocab):
    name = qin.get()
    while name != None:
        print 'parsing', name
	lines = open(name, 'r').readlines()
        if is_build_vocab:
            qout.put(dep.Dependency_Structure(lines).unique_words())
        else:
            qout.put(lines)
        print 'parsed', name
        name = qin.get()
    print 'dead'

def t_read(thread_num=100, upper=None, is_build_vocab=False):
    qout = Queue()
    qin = Queue()
    threads = []
    files = []
    files.extend(glob.glob(prenyt))
    files.extend(glob.glob(prewiki))
    if upper:
	files = files[:upper]
    for f in files:
        qout.put(f)
    start = time.clock()

    print 'gonna make ', min(thread_num, len(files)), ' threads'
    for _ in range(min(thread_num, len(files))):
        t = Thread(target=reader, args=(qout, qin, build_ds))
        t.start()
        threads.append(t)
        qout.put(None)

    text = []

    for _ in range(0, len(files)):
        text.extend(qin.get())
        print 'got text, total:', len(text)
    
    for t in threads:
        t.join()
    print 'total time:', str( time.clock() - start )
    print 'returning text', len(text)
    return text
