import dependency_structure as dep
import glob
#from Queue import Queue
from threading import Thread, Lock
from time import sleep
import time
from multiprocessing import Process, Queue

prenyt = '/data/mnt/ainos-research/corpus/nytimes/tree/*.cnlp'
prewiki = '/data/mnt/ainos-research/corpus/wikipedia2015/tree/*.cnlp'


def reader(qin, qout, lock, is_build_vocab=False, is_build_dep=False, is_context_analysis=False):
    with lock:
        name = qin.get()
    while name != None:
        print 'parsing', name
	lines = open(name, 'r')
        if is_build_vocab or is_build_dep or is_context_analysis:
            print 'building dep with '
            if is_build_vocab:
                ds = dep.Dependency_Structure(lines, is_file=False, is_text=True)
                with lock:
                    qout.put(ds.get_tokenized_sentences())
            elif is_build_dep:
                ds = dep.Dependency_Structure(lines, is_file=False, is_text=True)
                with lock:
                    qout.put(ds)
            elif is_context_analysis:
                ds = dep.Dependency_Structure(lines, is_file=False, is_text=False, is_context_analysis=True)
                print 'putting context of size', len(ds.context_data)
                qout.put(ds.context_data)
        else:
            with lock:
                qout.put(lines)
        print 'parsed', name
        name = qin.get()
    print 'dead'

def t_read(thread_num=1, upper=None, is_build_vocab=False, is_context_analysis=False):
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

    print 'gonna make ', min(thread_num, len(files)), ' threads'
    for _ in range(min(thread_num, len(files))):
        p = Process(target=reader, args=(qout, qin, lock, is_build_vocab, False, is_context_analysis))
        p.start()
        processes.append(p)
        qout.put(None)

    if not is_context_analysis:
        text = []
    else:
        res = []

    for p in processes:
        p.join()

    for _ in range(len(files)):
        if not is_context_analysis:
            res = qin.get()
            text.extend(res)
            print 'got text, total:', len(text)
        else:
            res.append(qin.get())
            print 'got output'
    
    print 'returning text'
    if is_context_analysis:
        return res
    else:
        return text

start = time.clock()
print t_read(is_context_analysis=True)
print 'total time:', str( time.clock() - start )

