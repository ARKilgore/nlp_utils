from gensim.models import Word2Vec
import threaded_reader as tr
import dependency_structure as dep
from time import clock

text = tr.t_read(threads=10)
print 'done reading'
start = clock()
ds = dep.Dependency_Structure(text, is_file=False, is_text=True, limit=100)
sentences = ds.get_tokenized_sentences()
print 'total ds time: ', str(start - clock())
model = Word2Vec(sentences, size=100, window=5, min_count=5, workers=16)
model.save('vectors_nyt.out')
