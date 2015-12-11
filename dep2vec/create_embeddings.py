from glob import glob
import cPickle as pickle
from gc import collect
from cosine_sim import Embedding_Similarity

fnames = glob('res/vector*')
terms = 'dat/verbs.txt'
for fname in fnames:
    emb = Embedding_Similarity(fname, terms)
    pickle.dump(emb, open(fname+'.emb.pkl', 'w'))
    emb = None
    print 'done: ', fname
    
