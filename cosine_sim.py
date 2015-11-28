import numpy as np
from gensim import models

def cosine_similarity(vector1, vector2):
    numerator = 0.0
    v1sum = 0.0
    v2sum = 0.0
    point1 = vector1.point
    point2 = vector2.point
    for s1, s2 in zip(np.nditer(point1, order='C', flags=['refs_ok']), np.nditer(point2, order='C', flags=['refs_ok'])):
        numerator += (s1 * s2)
        v1sum += (s1 * s1)
        v2sum += (s2 * s2)
        print 'num is ', numerator, ' s1, s2 are', s1, s2
    numerator /= v1sum
    numerator /= v2sum
    print 'ret ', numerator
    return numerator 

class Embedding_Similarity:
    def get_word_similarity(self, word1, word2):
        # accepts two words, returns their vector similarity if in corpus
        if word1 in self.term_to_index and word2 in self.term_to_index:
            return self.sim_matrix[self.term_to_index[word1]][self.term_to_index[word2]]
        else:
            return -2

    def sim_matrix_repeat(self, i, j, value):
        self.sim_matrix[i][j] = value
        self.sim_matrix[j][i] = value

    def __init__(self, vector_file, term_file, similarity_function=cosine_similarity):
        self.get_similarity = similarity_function
        self.vectors = {}
        self.term_to_index = {}

        model = models.Word2Vec.load(vector_file)
        for key in model.vocab:
            self.vectors[key] = model.vocab[key] # raw numpy vector, should work fine 
	print 'finished vector loading'

        with open(term_file, 'r') as w:
            self.terms = []
            for term in w:
                term = term.rstrip()
                if term in self.vectors:
                    print 'found ', term
                    self.terms.append(term)
                    self.term_to_index[term] = len(self.terms) - 1

	print 'finished finding terms, found', len(self.terms)
            
        self.sim_matrix = np.zeros((len(self.terms), len(self.terms)))

        for i, term1 in enumerate(self.terms):
            for j, term2 in enumerate(self.terms):
	        print 'comparing ', term1, term2
	        self.sim_matrix_repeat(i, j, self.get_similarity(self.vectors[term1], self.vectors[term2]))
	        print term1, term2, ': ', self.get_word_similarity(term1,term2)
	print 'done'

