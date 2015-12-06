import csv
from os import listdir
from os.path import isfile, join
import text_clean as tc

"""Loads dependency structure from file, give object-oriented representations"""

# Usage: Pass a file name to initialize Dependency_Structure with sentences.
# Sentences (node-based structure) can be accessed through Dependency_Structure.
# Most functionality to examine specfic structure and relations will happen at this level.

class Dependency_Structure:
    def ds_from_text(self, sentences, limit=None):
        chunk = []
        last_index = -1
        self.sentences = []
        for row in sentences:
            row = row.split('\t')
            if not row:
                if chunk:
                    self.sentences.append(Sentence(chunk))
                    chunk = []
                last_index = -1
                continue
            
            # Just for testing
            if limit and len(self.sentences) > limit:
                break

            if not row or len(row) < 1:
                continue
            if int(row[0]) > last_index:
                last_index = int(row[0])
                chunk.append(row)
            else:
                self.sentences.append(Sentence(chunk))
                last_index = -1
                chunk = [row]
        if chunk:
            self.sentences.append(Sentence(chunk))


    def ds_from_file(self, file_name, limit=None):
        last_index = -1
        # structure to hold sentence objects after processing
        self.sentences = []
        # chunk is a list of the words in the current sentence
        chunk = []
        with open(file_name, "r") as tsv_in:
            #tsv_in = csv.reader(tsv_in,delimiter='\t', quotechar='\x07')
            for row in tsv_in.readlines():
                row = row.split('\t')
                if not row:
                    if chunk:
                        self.sentences.append(Sentence(chunk))
                        chunk = []
                    last_index = -1
                    continue
                
                # TESTING ONLY
                if limit and len(self.sentences) > limit:
                    break
                #


                if not row or len(row) <= 1:
                    continue
                print row, len(row)
                if row and int(row[0]) > last_index:
                    last_index = int(row[0])
                    chunk.append(row)
                else:
                    self.sentences.append(Sentence(chunk))
                    last_index = -1
                    chunk = [row]
                    print 'break chunk here'
            if chunk:
                self.sentences.append(Sentence(chunk))



    def ds_from_dir(self, source, limit):
	files = [f for f in listdir(source) if isfile(join(source,f)) ]
        for f in files:
            self.ds_from_file(join(source + '/',f), limit)
	    print 'file complete'


    def get_tokenized_sentences(self):
        return [a.get_token_list() for a in self.sentences]

    def get_all_words(self):
        words = []
        for sentence in self.get_tokenized_sentences():
            for word in sentence:
                words.append(word)
        return words

    def unique(self):
        unique_tokens = {}
        for token in self.get_all_words():
            if token not in unique_tokens:
                unique_tokens[token] = 1
        return unique_tokens.keys()

    def get_sentences(self):
        return self.sentences

    def combine(self, ds):
        self.sentences = self.get_sentences() + ds.get_sentences()
        return self

    def combine_all(self, ds_list):
        """Extremely slow, need to optimize"""
        for ds in ds_list:
            combine(ds)
        return self
    
    def __init__(self, source, is_file=True, is_text=False, limit=None, stop_words=[]):
        # accepts name of tsv file containing dependency parsed corpus
        # track whether the current word (row) is the start of a new sentence

        if is_file:
            self.ds_from_file(source, limit)
        elif is_text:
            self.ds_from_text(source, limit)
        else:
            self.ds_from_dir(source, limit)
        print 'Created ', len(self.sentences), ' sentences'

class Sentence:
    def __init__(self, sentence, stop_words=[]):
	self.token_list = None
	self.nodes = None
	#for s in sentence:
#        sentence = [term.split('\t') for term in raw_text]
        nodes = [Node()]
        nodes.extend([Node() for i in range(0, len(sentence))])
        for i, term in enumerate(sentence, 1):
	    if term[1] in stop_words:
		nodes.remove(nodes[i])
		continue
            n = nodes[i]
            n.set_form(term[1])
            n.set_head(int(term[3]), term[4]) 
            n.set_pos(term[2])
            n.set_ne_tag(term[5])

            if n.head >= len(nodes):
                print 'ERROR ', i, n.head, n.form
                print sentence
            else:
                h = nodes[n.head]
                h.add_dep(i, n.arc)
        self.nodes = nodes

    def get_node(self, index):
        return self.nodes[index]

    def get_head(self, index):
        return self.nodes[self.nodes[index].get_head_index()]

    def get_siblings(self, index):
        if self.nodes[i].get_head_index() is -1:
            return []
        return self.nodes[self.nodes[index].get_head_index()].get_dep_list()

    def get_token_list(self):
	if not self.token_list:
	    self.token_list = []
	    for i, word in enumerate(self.nodes):
		if i != 0 and word.get_form() != None:
                    token = tc.clean(word.get_form())
                    if token:
	                self.token_list.append(token)
	return self.token_list

    def get_adjacency_context(self, which, window=-1):
        if window < 0:
            return [word.get_form() for i, word in enumerate(self.nodes) if i is not which]
        else:
            context_words = []
            for i in range(window, which+window):
                if i > -1 and i is not which and i < len(self.nodes):
                    context_words.append[self.nodes[i]]
            return context_words

    def get_dependency_context(self, which, window=-1):
        # temporary filler
        context = []
        # dependency features
        context.append(self.get_head(which))
        context.extend(self.get_siblings(which))

        return context

    def get_nodes_nohead(self, node=None):
	nodes = []
	for node in self.nodes:
	    if node.get_form() != None:
		nodes.append(node)
	return nodes

class Node:
    def __init__(self):
        self.head = None
        self.arc = None
        self.form = None
        self.pos = None
        self.ne_tag = None
        self.dep = []

    def set_ne_tag(self, tag):
        self.ne_tag = tag

    def set_form(self, form):
        self.form = form

    def set_pos(self, pos):
        self.pos = pos

    def set_head(self, head, arc): 
        #sets head INDEX not pointer to head
        self.head = head
        self.arc = arc

    def get_form(self):
        return self.form

    def get_token(self):
        return tc.clean(self.get_form())

    def add_dep(self, index, arc_type):
        self.dep.append((index, arc_type))

    def get_head_index(self):
        return self.head
        
    def get_head_arc(self):
        return self.arc

    def get_dep_list(self):
        return self.dep
    
    def is_verb(self):
        if self.pos and self.pos[0].lower() == 'v':
            return True
        else:
            return False
