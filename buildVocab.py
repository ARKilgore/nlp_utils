from gensim.models import Word2Vec
import threaded_reader as tr
import dependency_structure as dep
from time import clock

text = tr.t_read(thread_num=150, is_build_vocab=True)
print 'done reading'
start = clock()
print 'total ds time: ', str(clock() - start)
start = clock()
model = Word2Vec()
model.build_vocab(sentences)
print 'build vocab total time: ', str(clock() - start)
model.save('vectors.built_vocab')

