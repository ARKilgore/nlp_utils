from gensim.models import Word2Vec

f = open('nytimes.txt', 'r')
sentences = []
for line in f.readlines():
    sentences.append(line)
model = Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
model.save('vectors.out')
