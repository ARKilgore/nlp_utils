import csv
from os import listdir
from os.path import isfile, join
import text_clean as tc

"""Loads dependency structure from file, give object-oriented representations"""

# Usage: Pass a file name to initialize Dependency_Structure with sentences.
# Sentences (node-based structure) can be accessed through Dependency_Structure.
# Most functionality to examine specfic structure and relations will happen at this level.

class Dependency_Structure:
    def _chunk_builder(self, source, limit=None):
        chunk = []
        last_index = -1
        self.sentences = []
        for i, row in enumerate(source):
            row = row.split('\t')
            if not row:
                if chunk:
                    yield chunk
                    chunk = []
                last_index = -1
                continue
            if limit and len(self.sentences) > limit:
                break
            if row == ['\n']:
                continue
            if row and int(row[0]) > last_index:
                last_index = int(row[0])
                chunk.append(row)
            else:
                yield chunk
                last_index = -1
                chunk = [row]
        if chunk:
            yield chunk

    def ds_from_text(self, sentences, limit=None):
        print 'processing from text'
        for chunk in self._chunk_build(sentences, limit):
            self.sentences.append(Sentence(chunk))

    def ds_from_file(self, file_name, limit=None):
        print 'processing from file'
        f = open(file_name, 'r')
        self.ds_from_text(f, limit)
        f.close

    def ds_from_dir(self, source, limit):
        print 'processing from dir'
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

    def first_order_dep(self, sent):
        return sent.get_dependency_contexts('dep1')

    def first_second_order_dep(self, sent):
        return sent.get_dependency_contexts('dep2')

    def first_order_dep_h(self, sent):
        return sent.get_dependency_contexts('dep1h')

    def first_second_order_dep_h(self, sent):
        return sent.get_dependency_contexts('dep2h')

    def first_sib_dep(self, sent):
        return sent.get_dependency_contexts('sib1dep1')

    def first_sib_dep_h(self, sent):
        return sent.get_dependency_contexts('sib1dep1h')

    def semantic_head(self, sent):
        return sent.get_dependency_contexts('srl')

    def write_data_tuple(self, fp, tup):
        map(lambda x: fp.write(str(x) + ' '), tup)
        fp.write('\n')
    
    def write_data_tuple_list(self, fp, t_list):
        for t in t_list:
            self.write_data_tuple(fp, t)


    def context_analysis(self, source, context_type='dep1'):
        # assuming dep1 for now
        data = []
        fp = open('context_data_' + context_type + '.dat', 'w')
        # header write
        fp.write('w_index form POS context_word_index context_arc context_length\n')

        for chunk in self._chunk_builder(source, None):
            if len(data) > 100:
                self.write_data_tuple_list(fp, data)
                data = []
            sent = Sentence(chunk)
            contexts =  None
            contexts =  sent.get_dependency_contexts(context_type)
            if not contexts:
                continue
            for i, context in enumerate(contexts):
                if sent.nodes[i] == None:
                    continue
                # word index, form of contet, POS, index of context, arc of context, length of context
                for elem in context:
                    data.append( (i, elem[0], sent.nodes[int(elem[1])].pos, elem[1], elem[2], len(context)) )

        return 'context_data_'+context_type+'.dat'


    def ___context_analysis(self, context):
        get_contexts = { 'dep1'      :self.first_order_dep,
                        'dep2'      :self.first_second_order_dep,
                        'dep1h'     :self.first_order_dep_h,
                        'dep2h'     :self.first_second_order_dep_h,
                        'dep1sib1'  :self.first_sib_dep,
                        'dep1sib1h' :self.first_sib_dep_h,
                        'srl'       :self.semantic_head
                        }[context]
        data = []
        for i,sent in enumerate(self.sentences):
            for i, context in enumerate(get_contexts()):
                print float(i) / float(len(self.sentences))
                if sent.nodes[i] == None:
                    continue
                # word index, form of contet, POS, index of context, arc of context, length of context
                for elem in context:
                    data.append( (i, elem[0], self.nodes[elem[0]].pos, elem[1], elem[2], len(context)) )
                
                # Index list
                # Context size
                # Sentence size
                # Context words and POS
                count += len(context)
        return data
    
    def __init__(self, source, is_file=True, is_text=False, is_context_analysis=False, limit=None, stop_words=[]):
        # accepts name of tsv file containing dependency parsed corpus
        # track whether the current word (row) is the start of a new sentence

        if is_file:
            self.ds_from_file(source, limit)
        elif is_text:
            self.ds_from_text(source, limit)
        elif is_context_analysis:
            self.context_data = self.context_analysis(source)
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
            n.set_head(int(term[5]), term[6]) 
            n.set_pos(term[3])
            n.set_ne_tag(term[9])

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

    def get_dependency_context(self, word, context_type):
        # Returns list of (wordform, index, arc)
        if context_type == 'dep1':
            context = word.get_dep_list()
            full_context = []
            for pair in context:
                t = (self.nodes[pair[0]].form, pair[0], pair[1])
                full_context.append(t)
            context = full_context
        elif context_type == 'dep1h':
            context = word.get_dep_list()
            context.append(word.get_head_index())
            for pair in context:
                full_context.append( (self.nodes[pair[0]].form, pair[0], pair[1]) )
        elif context_type == 'sib1dep1':
            pass
        elif context_type == 'sib1dep1h':
            pass
        elif context_type == 'siball':
            pass
        elif context_type == 'srl':
            pass

        return context

    def get_dependency_contexts(self, context_type):
        contexts = []
        for word in self.nodes:
            contexts.append(self.get_dependency_context(word, context_type))
        return contexts

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


