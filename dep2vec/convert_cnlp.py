import csv, glob, os
from multiprocessing import Queue, Process
from operator import itemgetter

prenyt = '/data/mnt/ainos-research/corpus/nytimes/tree/*.cnlp'
prewiki = '/data/mnt/ainos-research/corpus/wikipedia2015/tree/*.cnlp'

pathnyt = '/data/mnt/ainos-research/corpus/nytimes/tree/'
pathwiki = '/data/mnt/ainos-research/corpus/wikipedia2015/tree/'

cols = [0, 1, 3, 5, 6, 9]

def convert(fname):
    fout = fname.split('.cnlp')[0] + '.snlp'
    with open(fname, 'r') as f, open(fout, 'w') as out:
        f = csv.reader(f, delimiter='\t', quotechar='\x07')
        out = csv.writer(out, delimiter='\t', quotechar='\x07')
        for i, row in enumerate(f):
            if not row:
                out.writerow([])
                continue
            row = list(itemgetter(*cols)(row))
            row[-1] = row[-1].rstrip()
            out.writerow(row)
    os.remove(fname)

def convert_worker(jobs):
    job = jobs.get()
    while job != None:
        convert(job)
        job = jobs.get()


def convert_all(threads=100):
    fnames = []
    fnames.extend(glob.glob(prenyt))
    fnames.extend(glob.glob(prewiki))
    jobs = Queue()
    for fname in fnames:
        jobs.put(fname)

    ps = []
    for _ in range(min(threads, len(fnames))):
        p = Process(target=convert_worker, args=(jobs,))
        jobs.put(None)
        ps.append(p)

    [p.start() for p in ps]
convert('nyt_000_sentences.cnlp')
