import cPickle as pickle
from glob import glob
from cosine_sim import average_vectors

embfiles = glob('res/*.pkl')
#embfiles = [embfiles[0]]
print embfiles
embeddings = []

for embfile in embfiles:
    embeddings.append(pickle.load(open(embfile, 'r')))
    print 'finished ', embfile

average = average_vectors(embeddings)


pickle.dump(average, open('res/averaged_0_9.pkl', 'w'))
