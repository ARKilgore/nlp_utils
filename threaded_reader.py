import dependency_structure as dep
import glob
from Queue import Queue
from threading import Thread
from multiprocessing.pool import ThreadPool
from time import sleep
import time

prenyt = '/data/mnt/ainos-research/corpus/nytimes/tree/*.cnlp'
prewiki = '/data/mnt/ainos-research/corpus/wikipedia2015/tree/*.cnlp'


def reader(qin, qout, is_build_vocab=False, is_build_dep=False):
    name = qin.get()
    while name != None:
        print 'parsing', name[:10]
	lines = open(name, 'r').readlines()
        if is_build_vocab or is_build_dep:
            ds = dep.Dependency_Structure(lines, is_file=False, is_text=True)
            if is_build_vocab:
                qout.put(ds.get_tokenized_sentences())
            elif is_build_dep:
                qout.put(ds)
        else:
            qout.put(lines)
        print 'parsed', name
        name = qin.get()
    print 'dead'

def t_read(thread_num=100, upper=None, is_build_vocab=False):
    qout = Queue()
    qin = Queue()
    threads = []
    files = ['nyt_000_sentences.cnlp']
#    files.extend(glob.glob(prenyt))
#    files.extend(glob.glob(prewiki))
    if upper:
	files = files[:upper]
    for f in files:
        qout.put(f)
    start = time.clock()

    print 'gonna make ', min(thread_num, len(files)), ' threads'
    for _ in range(min(thread_num, len(files))):
        t = Thread(target=reader, args=(qout, qin, is_build_vocab))
        t.start()
        threads.append(t)
        qout.put(None)

    text = []

    for t in threads:
        t.join()

    for _ in range(0, len(files)):
        res = qin.get()
        print res
        text.extend(res)
        print 'got text, total:', len(text)
    
    print 'total time:', str( time.clock() - start )
    print 'returning text', len(text)
    return text
