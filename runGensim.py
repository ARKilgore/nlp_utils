from gensim.models import Word2Vec
import threaded_reader as tr
import dependency_structure as dep
from time import clock
from buildVocab import build_vocab
import glob
from threading import Thread
from Queue import Queue

"""Build Vocab"""
start = clock()
text = tr.t_read(thread_num=100, is_build_vocab=True)
print 'total read time: ', str(clock() - start)
print 'done reading'
#ds = dep.Dependency_Structure(text, is_file=False, is_text=True)
model = Word2Vec(text, workers=16)
# model.build_vocab(text)
print 'total v build time: ', str(clock() - start)

"""Generate dep_structures from threads, train as they finish"""
#start = clock()
#threads = []
#files = ['nyt_000_sentences.cnlp']
##files.extend(glob.glob('/data/mnt/ainos-research/corpus/nytimes/tree/*.cnlp'))
##files.extend(glob.glob('/data/mnt/ainos-research/corpus/wikipedia2015/tree/*.cnlp'))
#
#qin = Queue()
#qout = Queue()
#
#for f in files:
#    qout.put(f)
#
#for i in range(min(100, len(files))):
#    t = Thread(target=tr.reader, args=(qout, qin, False, True))
#    t.start()
#    threads.append(t)
#    qout.put(None)
#
#for _ in range(len(files)):
#    ds = qin.get()
#    model.train(ds.get_tokenized_sentences)
#
#for t in threads:
#    t.join()

print 'word2vec, 16 workers, total time: ', str(clock() - start)
model.save('vectors.out.onetest')

