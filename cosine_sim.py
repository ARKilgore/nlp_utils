import numpy as np
from gensim import models
from math import sqrt

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

    def __init__(self, vector_file, term_file):
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
                    #print 'found ', term
                    self.terms.append(term)
                    self.term_to_index[term] = len(self.terms) - 1

	print 'finished finding terms, found', len(self.terms)
            
        self.sim_matrix = np.zeros((len(self.terms), len(self.terms)))

        for i, term1 in enumerate(self.terms):
            for j, term2 in enumerate(self.terms):
	        print 'comparing ', term1, term2
	        self.sim_matrix_repeat(i, j, model.similarity(term1,term2))
	        #print term1, term2, ': ', self.get_word_similarity(term1,term2)
	print 'done'

