import csv

class Dependency_Structure:
    def __init__(self, file_name):
        # accepts name of tsv file containing dependency parsed corpus
        # track whether the current word (row) is the start of a new sentence
        last_index = -1
        # structure to hold sentence objects after processing
        self.sentences = []
        # chunk is a list of the words in the current sentence
        chunk = []
        with open(file_name, "r") as tsv_in:
            tsv_in = csv.reader(tsv_in, delimiter = '\t')
            for row in tsv_in:
                if int(row[0]) > last_index:
                    last_index = int(row[0])
                    chunk.append(row)
                else:
                    self.sentences.append(Sentence(chunk))
                    last_index = int(row[0])
                    chunk = [row]
            if chunk:
                self.sentences.append(Sentence(chunk))

class Sentence:
    def __init__(self, raw_text)
        sentence = [term.split('\t') for term in raw_text]
        nodes = [Node() for i in range(0, len(sentence)]
        for i, term in enumerate(sentence):
            n = nodes[i]
            n.set_form(term[1])
            n.set_head(term[5], term[6]) # not sure whether to use malt or stanford, this is malt
            
            h = nodes[n.head]
            h.add_dep(i, n.arc)
        self.nodes = nodes

    def get_head(self, index):
        return self.nodes[self.nodes[index].get_head_index()]

    def get_siblings(self, index):
        if self.nodes[i].get_head_index() is -1:
            return []
        return self.nodes[self.nodes[index].get_head_index()].get_dep_list()

    def get_adjacency_context(self, which, window=-1):
        if window < 0:
            return [word.get_form() for i, word in enumerate(self.nodes) if i is not which]
        else:
            context_words = []
            for i in range(window, which+window):
                if i > -1 and i is not which and i < len(self.nodes):
                    context_words.append[self.nodes[i]
            return context_words

    def get_dependency_context(self, which, window=-1):
        # temporary filler
        return get_head(which)

class Node:
    def __init__(self):
        self.head = None
        self.arc = None
        self.form = None
        self.dep = []
    
    def set_form(self, form):
        self.form = form

    def set_head(self, head, arc):
        self.head = head
        self.arc = arc

    def get_form():
        return self.form

    def add_dep(self, index, arc_type):
        self.dep.append((index, arc_type))

    def get_head_index():
        return self.head
        
    def get_head_arc():
        return self.arc

    def get_dep_list():
        return self.dep
        
