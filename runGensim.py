from gensim.models import Word2Vec
import threaded_reader as tr
import dependency_structure_s as dep
from time import clock
from buildVocab import build_vocab
import glob, zlib
from threading import Thread
from Queue import Queue

"""Build Vocab"""
start = clock()
text = tr.simple_read(100) # number of things in redis
print 'total read time: ', str(clock() - start)
print 'done reading'
#ds = dep.Dependency_Structure(text, is_file=False, is_text=True)
model = Word2Vec.load('vectors.baseline')
print 'total v build time: ', str(clock() - start)

start = clock()
model.train(dep.Dependency_Structure(text, is_file=False, is_text=True).get_tokenized_sentences())

print 'word2vec, total time: ', str(clock() - start)
model.save('vectors.out.pleasework')

