import nltk
from nltk.classify import SklearnClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
import cPickle as pickle
import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction import DictVectorizer
import pandas as pd
import numpy as np

all_words = []

def extract_features_dict(text=None, is_raw=False):
    if is_raw:
        text = text.split(' ')

    features = {}
    #word_feature = lambda x: 'contains(%s)' % x

    text_set = set(text)
    print 'inner feature extraction'
    for i, word in enumerate(all_words):
	if word in text_set:
	    features[i] = 1
        else:
	    features[i] = 0
        #features[i] = (word in text_set)
    print 'returning dict features'
    return features

"""
    # Negations
    negations = ['but', 'not', 'almost', 'except']
    word_set = set(text)
    for negation in negations:
        if negation in word_set:
            features['contains(%s)' % negation] = True
        else:
            features['contains(%s)' % negation] = False
"""

    # Adjectives
    # adjectives = []
    # with open('adj', 'r') as adjectives_file:
    #     for adjective in adjectives_file.readlines():
    #         adjectives.append(adjective.lower().rstrip())

    # for adjective in adjectives:
    #     if adjective in word_set:
    #         features['contains(%s)' % adjective] = True
    #     else
    #         features['contains(%s)' % adjective] = False


def use_feature_dicts(train_x, is_raw = True):
    train_x_dicts = []
    for x in train_x:
        print 'extracting dict'
        train_x_dict = extract_features_dict(x, is_raw = is_raw)
        train_x_dicts.append(train_x_dict)
    # print train_x_dicts
    vec = DictVectorizer()
    print 'transforming...'
    return vec.fit_transform(train_x_dicts)

def word_to_set(phrase_list, is_raw=False, trim = 1):
    words_list = []
    words_count = {}
    for phrase in phrase_list:
        for word in phrase.split():
            token = word.lower().rstrip()
            if token in words_count:
                words_count[token] += 1
            else:
                words_count[token] = 1
            if words_count[token] == trim:
                words_list.append(token)

    return list(set(words_list))

def main():
    print 'getting train'
    train = pd.read_csv('dat/train.tsv',sep = '\t')
    print 'getting test'
    test = pd.read_csv('dat/dev.tsv', sep = '\t')

    global all_words
    all_words = word_to_set(train['Phrase'], trim=5, True)

    print 'creating x dict vectors from train'
    train_x = train['Phrase']
    print 'extracting...'
    train_x = use_feature_dicts(train_x)
    # print train_x

    print 'creating train y'
    train_y = [int(y) for y in train['Sentiment']]
    # print train_y

    # count_vector = CountVectorizer()
    # train_counts = count_vector.fit_transform(train['Phrase'])
    # tfidf_vectorizer = TfidfTransformer()
    # # print 'tfidf train x'
    # # train_vectors = tfidf_vectorizer.fit_transform(train_x)
    # # print 'trainsform train x'
    # # test_vectors = tfidf_vectorizer.transform(train_vectors)
    # classifier = MultinomialNB().fit(train_vectors, train['Sentiment'])
    print 'classifying'
    classifier = MultinomialNB().fit(train_x, train_y)
    
    # x_test_counts = count_vector.transform(test['Phrase'])
    # test_vector = tfidf_vectorizer.transform(x_test_counts)

    print 'testing'
    test_x = use_feature_dicts(test['Phrase'])
    
    #test_x = raw_input('test...')
    #while test_x != "q":
    #    print classifier.predict(use_feature_dicts([test_x], True))
    #    test_x = raw_input('test...')
    #return
    for i in predicted:
        print i
    pickle.dump(classifier, open('multinomialNB.pickle', 'w'))

main()


"""READING IN FROM FILES"""

# def read_train(source):
#     # open data file
#     # discard header line
#     fdata = open(source, 'r')
#     fdata.readline()
    
#     phrases = []
#     phrase_to_id = {}
#     for data in fdata:
#         data = data.split('\t')
#         phrases.append(([token.lower().rstrip() for token in data[2].split(' ')],int(data[3].rstrip())))
#         phrase_to_id[data[2].lower().rstrip()] = data[0]
#     return phrases, id_to_phrase


# def read_data(source='', which='train'):

#     phrases, phrase_to_id = {
#         'train': read_train,
#         'dev': 'dev',   # unimplemented TODO 
#         'test': 'test' # unimplemented TODO 
#     }[which](source)

#     return phrases, phrase_to_id
#     fdata.close()

    
# """WORD AND FEATURE EXTRACTION""" 
# def get_phrase_list(sent_tups, with_label=False):
#     phrases = []
#     for s_tup in sent_tups:
#         if not with_label:
#             phrases.append(' '.join(s_tup[0]))
#         else:
#             phrases.append((' '.join(s_tup[0]), s_tup[1]))
#     return phrases

# def get_all_words(sent_tups):
#     all_words = []
#     for sent_tup in sent_tups:
#         words, _ = sent_tup
#         all_words.extend(words)
#     return all_words

# def get_features(words):
#     words = nltk.FreqDist(words)
#     features = words.keys()
#     return features

# global_features = {}
# adjectives

# def extract_features(doc):
#     words = set(doc)
#     features = {}
    
#     for i, word in enumerate(global_features):
#         features[i] = int(word in words)
#         #features['contains(%s)' % word] = (word in words)
    
#     for i, word in enumerate(adjective):
#         features[i+len(global_features)] = int(adj in words)
#     return features

# def main(which='NB'):
#     print 'reading training data'
#     training_data, phrase_to_id = read_data(source='dat/train.tsv')

#     print 'getting features'
#     global global_features 
#     global adjectives
#     global_features = get_features(get_all_words(training_data))
#     with open('adj', 'r') as adj_file:
#         for adj in adj_file:
#             adjectives.append(adj.lower().rstrip())
#     print 'entering switch'
#     if which == 'NB':
#         training_set = nltk.classify.util.apply_features(extract_features, get_phrase_list(training_data, True)) 
#         print 'moving to classifier creation'
#         start = time.clock()
#         classifier = nltk.NaiveBayesClassifier.train(training_set)
#         print 'classfier total time: ', str(time.clock() - start)
#         #classifier = SklearnClassifier(BernoulliNB()).train(training_set)
 
#         pickle.dump(classifier, open('classifier.pickle', 'w'))
               
#         text = raw_input('Next test (q to quit):')
#         while text != 'q':
#             print classifier.classify(extract_features(text.split()))
# 	    text = raw_input('Next test (q to quit):')
#     elif which == 'SGD':
#         print 'extracting features'
# 	training_set = nltk.classify.util.apply_features(extract_features, get_phrase_list(training_data)) 
#         training_list = []
#         for d in training_set:
#             sample = []
#             for k, v in d.iteritems():
#                 sample.append(v)
#             training_list.append(sample)
#         label_set = [int(tup[1]) for tup in training_data]
# 	print 'moving to classifier creation'
#         clf = SGDClassifier(loss="hinge", penalty="l2")
# 	print 'moving to training'
#         clf.fit(training_list, label_set)
#         pickle.dump(clf, open('sgd_sent.pickle', 'w'))
 
# 	print 'moving to prediction'
#         pred =[]
#         pred.append('i hate everyhing')
#         pred.append('i love everything')
#         pred_set = nltk.classify.util.apply_features(extract_features, pred)
#         pred_list = []
#         print pred_set
#         for d in pred_set:
#             inst_list = []
# 	    for k, v in d.iteritems():
#                 inst_list.append(v)
#             pred_list.append(inst_list)
#         print pred_list
#         print clf.predict(pred_list)
        

# main(which='SGD')
