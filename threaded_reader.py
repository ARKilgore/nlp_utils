import dependency_structure as dep
import glob
#from Queue import Queue
from threading import Thread, Lock
from time import sleep
import time
from multiprocessing import Process, Queue

prenyt = '/data/mnt/ainos-research/corpus/nytimes/tree/*.cnlp'
prewiki = '/data/mnt/ainos-research/corpus/wikipedia2015/tree/*.cnlp'


def reader(qin, qout, lock, is_build_vocab=False, is_build_dep=False, is_count_context=False):
    with lock:
        name = qin.get()
    while name != None:
        print 'parsing', name[10:]
	lines = open(name, 'r').readlines()
        if is_build_vocab or is_build_dep or is_count_context:
            ds = dep.Dependency_Structure(lines, is_file=False, is_text=True)
            if is_build_vocab:
                with lock:
                    qout.put(ds.get_tokenized_sentences())
            elif is_build_dep:
                with lock:
                    qout.put(ds)
            elif is_count_context:
                qout.put(ds.get_context_size('dep1'))
        else:
            with lock:
                qout.put(lines)
        print 'parsed', name
        with lock:
            name = qin.get()
    print 'dead'

def t_read(thread_num=100, upper=None, is_build_vocab=False, is_count_context=False):
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
    for _ in range(min(thread_num, len(files))):
        p = Process(target=reader, args=(qout, qin, lock, is_build_vocab, is_count_context))
        p.start()
        processes.append(p)
        qout.put(None)

    if not is_count_context:
        text = []
    else:
        res = (0, 0)

    for p in processes:
        p.join()

    for _ in range(len(files)):
        if not is_count_context:
            res = qin.get()
            text.extend(res)
            print 'got text, total:', len(text)
        else:
            words, total_c = qin.get()
            res = (res[0] + words, res[1] + total_c)
    
    print 'total time:', str( time.clock() - start )
    print 'returning text'
    if is_count_context:
        return res
    else:
        return text
