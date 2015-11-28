import numpy as np
from gensim import models

def cosine_similarity(vector1, vector2):
    numerator = 0
    v1sum = 0
    v2sum = 0
    for s1, s2 in zip(vector1, vector2):
        numerator += s1 * s2
        v1sum += s1**2
        v2sum += s2**2
    return numerator / (v1sum * v2sum)

class Embedding_Similarity:
    def get_word_similarity(self, word1, word2):
        # accepts two words, returns their vector similarity if in corpus
        if word1 in self.term_to_index and word2 in self.term_to_index:
            return self.sim_matrix[self.term_to_index[term1]][self.term_to_index[term2]]
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
        print 'woman:', self.vectors['woman'], model.vocab['woman']

        with open(term_file, 'r') as w:
            self.terms = []
            for term in w:
                if term in self.vectors:
                    print 'found ', term
                    self.terms.append(term)
                    self.term_to_index[term] = len(self.terms) - 1
            
        self.sim_matrix = np.zeros((len(self.terms), len(self.terms)))
        for i, term1 in enumerate(self.terms):
            for j, term2 in enumerate(self.terms):
                if i == j:
                    self.sim_matrix[i][j] = 1
                if self.sim_matrix[i][j] != 0:
                    self.sim_matrixrepeat(i, j, self.get_similarity(self.vectors[term1],
                                                                self.vectors[term2]
                                                                ))

