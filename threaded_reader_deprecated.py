import dependency_structure as dep
import glob
#from Queue import Queue
from threading import Thread, Lock
from time import sleep
import time
from multiprocessing import Process, Queue

prenyt = '/data/mnt/ainos-research/corpus/nytimes/tree/*.cnlp'
prewiki = '/data/mnt/ainos-research/corpus/wikipedia2015/tree/*.cnlp'


def reader(qin, qout, lock, is_build_vocab=False, is_build_dep=False):
    with lock:
        name = qin.get()
    while name != None:
        print 'parsing', name[10:]
	lines = open(name, 'r').readlines()
        if is_build_vocab or is_build_dep:
            ds = dep.Dependency_Structure(lines, is_file=False, is_text=True)
            if is_build_vocab:
                with lock:
                    qout.put(ds.get_tokenized_sentences())
            elif is_build_dep:
                with lock:
                    qout.put(ds)
        else:
            with lock:
                qout.put(lines)
        print 'parsed', name
        with lock:
            name = qin.get()
    print 'dead'

def t_read(thread_num=100, upper=None, is_build_vocab=False):
    qout = Queue()
    qin = Queue()
    processes = []
    files = []
    lock = Lock()
#    files = ['nyt_000_sentences.cnlp']
    files.extend(glob.glob(prenyt))
    files.extend(glob.glob(prewiki))
    if upper:
	files = files[:upper]
    for f in files:
        qout.put(f)
    start = time.clock()

    print 'gonna make ', min(thread_num, len(files)), ' threads'
    for c in range(min(thread_num, len(files))):
        p = Process(target=reader, args=(qout, qin, lock, is_build_vocab))
        p.start()
        processes.append(p)
        qout.put(None)
	print c

    text = []
    print 'joining'
    for p in processes:
        p.join()

    for c in range(len(files)):
        res = qin.get()
        text.extend(res)
        print 'got text, total:', len(text), ' num: ', c
    
    print 'total time:', str( time.clock() - start )
    print 'returning text', len(text)
    return text
