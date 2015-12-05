import glob
from time import sleep, clock
from multiprocessing import Process, Queue
import redis

prenyt = '/data/mnt/ainos-research/corpus/nytimes/tree/*.cnlp'
prewiki = '/data/mnt/ainos-research/corpus/wikipedia2015/tree/*.cnlp'


def reader(jobs, out):
    name = jobs.get()
    
    while name != None:
        print 'parsing', name[20:]
        with open(name, 'r') as f:
            lines = f.readlines()
        out.put(lines)
        
        print 'parsed', name
        name = jobs.get()
    print 'dead'

def t_read(thread_num=100, upper=None, files=None):
    jobs = Queue()
    results = Queue()
    processes = []
    
    #if not files:
    #    files = []
    #    files = ['nyt_000_sentences.cnlp']
#    files.extend(glob.glob(prenyt))
#    files.extend(glob.glob(prewiki))

    if upper:
	files = files[:upper]

    for f in files:
        jobs.put(f)

    start = clock()

    print 'gonna make ', min(thread_num, len(files)), ' threads'

    for _ in range(min(thread_num, len(files))):
        p = Process(target=reader, args=(jobs, results))
        p.start()
        processes.append(p)
        jobs.put(None)

    text = []
    for _ in files:
        text.extend(results.get())

    
    print 'total time:', str(clock() - start )
    print 'returning text', len(text)
    return text

