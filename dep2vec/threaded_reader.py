import glob
from time import sleep, clock
from multiprocessing import Process, Queue
import redis

prenyt = '/data/mnt/ainos-research/corpus/nytimes/tree/*.cnlp'
prewiki = '/data/mnt/ainos-research/corpus/wikipedia2015/tree/*.cnlp'


def reader(jobs, out):
    index, name = jobs.get()
    
    while name != None:
        print 'parsing', name[10:]
        with open(name, 'r') as f:
            lines = f.readlines()
        out.set(index, lines)
        
        print 'parsed', name
        name = jobs.get()
    print 'dead'

def t_read(thread_num=100, upper=None):
    jobs = Queue()
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    processes = []

    files = []
    files = ['nyt_000_sentences.cnlp']
#    files.extend(glob.glob(prenyt))
#    files.extend(glob.glob(prewiki))

    if upper:
	files = files[:upper]

    for i, f in enumerate(files):
        jobs.put((i, f))
    print 'there are ', i, ' files'

    start = clock()

    print 'gonna make ', min(thread_num, len(files)), ' threads'

    for _ in range(min(thread_num, len(files))):
        p = Process(target=reader, args=(jobs, r))
        p.start()
        processes.append(p)
        jobs.put(None)

    for p in processes:
        p.join()

    
    print 'total time:', str( time.clock() - start )
    print 'returning text', len(text)
    return r, len(files)
