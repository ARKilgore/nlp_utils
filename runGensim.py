from gensim.models import Word2Vec
import threaded_reader as tr
import dependency_structure as dep
from time import clock
from buildVocab import build_vocab

model = build_vocab()
text = tr.t_read(thread_num=100, upper = 1)
fs = []
fs.extend
print 'done reading'
start = clock()
ds = dep.Dependency_Structure(text, is_file=False, is_text=True)
print 'total ds time: ', str(clock() - start)
sentences = ds.get_tokenized_sentences()
start = clock()
model = Word2Vec(sentences, workers=16)
print 'word2vec, 16 workers, total time: ', str(clock() - start)
model.save('vectors.out')

