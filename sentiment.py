import nltk
from nltk.classify import SklearnClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import BernoulliNB
import cPickle as pickle
import time

"""READING IN FROM FILES"""
def read_train(source):
    # open data file
    # discard header line
    fdata = open(source, 'r')
    fdata.readline()
    
    phrases = []
    for data in fdata:
        data = data.split('\t')
        phrases.append(([token.lower().rstrip() for token in data[2].split(' ')],int(data[3].rstrip())))
    return phrases


def read_data(source='', which='train'):

    phrases = {
        'train': read_train,
        'dev': 'dev',   # unimplemented TODO 
        'test': 'test' # unimplemented TODO 
    }[which](source)

    return phrases
    fdata.close()

    
"""WORD AND FEATURE EXTRACTION""" 
def get_phrase_list(sent_tups, with_label=False):
    phrases = []
    for s_tup in sent_tups:
        if not with_label:
            phrases.append(' '.join(s_tup[0]))
        else:
            phrases.append((' '.join(s_tup[0]), s_tup[1]))
    return phrases

def get_all_words(sent_tups):
    all_words = []
    for sent_tup in sent_tups:
        words, _ = sent_tup
        all_words.extend(words)
    return all_words

def get_features(words):
    words = nltk.FreqDist(words)
    features = words.keys()
    return features

global_features = {}

def extract_features(doc):
    words = set(doc)
    features = {}
    for i, word in enumerate(global_features):
        features[i] = int(word in words)
        #features['contains(%s)' % word] = (word in words)
    return features

def main(which='NB'):
    print 'reading training data'
    training_data = read_data(source='dat/train.tsv')

    print 'getting features'
    global global_features 
    global_features = get_features(get_all_words(training_data))
    
    print 'entering switch'
    if which == 'NB':
        training_set = nltk.classify.util.apply_features(extract_features, get_phrase_list(training_data, True)) 
        print 'moving to classifier creation'
        start = time.clock()
        classifier = nltk.NaiveBayesClassifier.train(training_set)
        print 'classfier total time: ', str(time.clock() - start)
        #classifier = SklearnClassifier(BernoulliNB()).train(training_set)
 
        pickle.dump(classifier, open('classifier.pickle', 'w'))
               
        text = raw_input('Next test (q to quit):')
        while text != 'q':
            print classifier.classify(extract_features(text.split()))
	    text = raw_input('Next test (q to quit):')
    elif which == 'SGD':
        print 'extracting features'
	training_set = nltk.classify.util.apply_features(extract_features, get_phrase_list(training_data)) 
        training_list = []
        for d in training_set:
            sample = []
            for k, v in d.iteritems():
                sample.append(v)
            training_list.append(sample)
        label_set = [int(tup[1]) for tup in training_data]
	print 'moving to classifier creation'
        clf = SGDClassifier(loss="hinge", penalty="l2")
	print 'moving to training'
        clf.fit(training_list, label_set)
        pickle.dump(clf, open('sgd_sent.pickle', 'w'))
 
	print 'moving to prediction'
        pred =[]
        pred.append('i hate everyhing')
        pred.append('i love everything')
        pred_set = nltk.classify.util.apply_features(extract_features, pred)
        pred_list = []
        print pred_set
        for d in pred_set:
            inst_list = []
	    for k, v in d.iteritems():
                inst_list.append(v)
            pred_list.append(inst_list)
        print pred_list
        print clf.predict(pred_list)
        

main(which='SGD')
