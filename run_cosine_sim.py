import cosine_sim as cs

def make():
    return cs.Embedding_Similarity('vectors.baseline', 'verbs.txt')

make()
