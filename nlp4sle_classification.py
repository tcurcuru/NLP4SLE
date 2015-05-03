# -*- coding: utf-8 -*-

"""
cosi140b - NLP4SLE - Machine Learning
Classification Module

Reference:
http://nbviewer.ipython.org/github/tpeng/python-crfsuite/blob/master/examples/CoNLL%202002.ipynb
"""

from __future__ import print_function
import pycrfsuite
import time
from collections import Counter
from nlp4sle_features import extract_features
from nlp4sle_evaluation import Metrics_BIO
from sklearn.metrics import classification_report, confusion_matrix

class Classification():
    """ Classification """
    def __init__(self):
        self.model = str() #name of model file
    
    def train(self,data_dir,model_file):
        """ Train data_file and save model in model_file """
        self.model = model_file
        
        features,labels = extract_features(data_dir)        
        
        trainer = pycrfsuite.Trainer(verbose=False)
        for f,l in zip(features,labels):
            trainer.append(f,l)
        
        t0 = time.time()
        trainer.train(self.model)
        dt = time.time() - t0
        print('Total training time: %d seconds' % dt)

    def tagger(self):
        """ CRF Tagger """
        t = pycrfsuite.Tagger()
        t.open(self.model)
        return t 

    def decode_sent(self,sent_features,tagger):
        """ Predict bio tags for words in a sentence """
        return tagger.tag(sent_features)

    def decode(self,data_dir,mode='decode'):
        """ Predict bio tags for words in data_file """
        features,labels = extract_features(data_dir,mode)
        
        t = self.tagger()
        predicted = list()
        t0 = time.time()
        for sf in features:
            predicted.extend(self.decode_sent(sf,t))
        dt = time.time() - t0
        print('Total decoding time: %d seconds' % dt)
        
        correct = list()
        if mode=='train':            
            for sl in labels:
                correct.extend(sl)
        return predicted,correct

    def evaluate(self,gold_dir):
        """ Return evaluation metrics for test data """
        predicted,correct = self.decode\
                            (gold_dir,mode='train')
        print('\nsklearn classification report:')
        print(classification_report(correct,predicted))
        print('\nsklearn confusion matrix:')
        print(confusion_matrix(correct,predicted))
        m = Metrics_BIO(predicted,correct) 
        return m.precision(),m.recall(),m.f_measure()

    def print_f(self,features):
        """ Print features in model """
        for (a1,a2),w in features:
            print('{0:10.5f}\t{1:20s}{2:s}'.format(w,a1,a2))

    def s_f(self):
        """ Return sorted list of state features in model """
        return Counter(self.tagger().info().state_features).\
               most_common()

    def t_f(self):
        """ Return sorted list of transitions in model """
        return Counter(self.tagger().info().transitions).\
               most_common()    

if __name__ == "__main__":    
    data_dir = 'train'
    model = 'nlp4sle.crfsuite'
    c = Classification()
    c.train(data_dir,model)    
    #c.model = model
    e1,e2,e3 = c.evaluate(data_dir)
    print('Overall results: ')
    print('{0:15s}{1:15s}{2:15s}'.format('Precision',\
            'Recall','F-measure'))
    print('{0:7.2f}        {1:7.2f}        {2:7.2f}'.\
          format(e1,e2,e3))
    print('\nTop likely transitions:')
    c.print_f(c.t_f()[:10])
    print('Top unlikely transitions:')
    c.print_f(c.t_f()[-10:])
    print('\nTop positive:')
    c.print_f(c.s_f()[:10])
    print('Top negative:')
    c.print_f(c.s_f()[-10:])
