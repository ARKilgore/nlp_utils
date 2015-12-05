from gensim.models import Word2Vec
from nlp_utils.dep2vec import threaded_reader as tr
from nlp_utils.dep2vec import dependency_structure_s as dep
from time import clock
from multiprocessing import Process
import glob

prenyt = '/data/mnt/ainos-research/corpus/nytimes/tree/*.snlp'
prewiki = '/data/mnt/ainos-research/corpus/wikipedia2015/tree/*.snlp'

nyt = glob.glob(prenyt)
wiki = glob.glob(prewiki)

file_lists = []
lower = 0
incr = 17
upper = incr
def chunker(flist, lower, upper, incr):
    file_lists = []
    while upper < len(flist):
        file_lists.append(flist[lower:upper])
        lower += incr
        upper += incr
    else:
        file_lists.append(flist[lower:])
    return file_lists
file_lists.extend(chunker(nyt, lower, upper, incr))
file_lists.extend(chunker(wiki, lower, upper, incr))
print len(file_lists)

#file_lists = [nyt1, nyt2, wiki1, wiki2, wiki3, wiki4, wiki5]
#file_lists = [[file_lists[0]]]
model = Word2Vec.load('vectors.baseline')
"""Build Vocab"""
start = clock()
for i, fileset in enumerate(file_lists):
    print 'working on ', len(fileset), ' files'
    text = tr.t_read(30, files=fileset) 
    print 'total read time: ', str(clock() - start)
    print 'done reading'
    ds = dep.Dependency_Structure(text, is_file=False, is_text=True)
    print 'total v build time: ', str(clock() - start)
    
    start = clock()
    model.train(dep.Dependency_Structure(text, is_file=False, is_text=True).get_tokenized_sentences())
    
    print 'word2vec, total time: ', str(clock() - start)
    fname = '/data/vectors.' + str(i)
    model.save(fname)

