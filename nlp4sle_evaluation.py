# -*- coding: utf-8 -*-

"""
cosi140b - NLP4SLE - Machine Learning
Evaluation Module

Reference:
http://en.wikipedia.org/wiki/Precision_and_recall

Demo:
>>> m.recall()
60.0
>>> m.precision()
60.0
>>> m.f_measure()
60.0
"""

from __future__ import division

class Metrics_BIO():
    """
    Token-level metrics for BIO tagger evaluation
    'O' (and '') label discarded
    """
    def __init__(self,correct=[],predicted=[]):
        if len(correct)==len(predicted):
            # list of correct tags
            self.c = correct
            # list of predicted tags
            self.p = predicted
        else:
            self.c = []
            self.p = []
            print 'Your input is invalid:'
            print 'len(correct)!=len(predicted)'
            print 'Please assign your input values later:'
            print '[self].c = correct'
            print '[self].p = predicted'
            
    def bio_tags(self,tag_list):
        """ -> set of indexes of bio tags """
        if len(tag_list)>0:
            indexes = set()
            for i,tag in enumerate(tag_list):
                if tag!='O' and tag!='':
                    indexes.add(i)
            return indexes
        else:
            raise ValueError('Empty input list!')

    def relevant_elements(self):
        """ -> set of indexes of relevant elements """        
        return self.bio_tags(self.c)

    def selected_elements(self):
        """ -> set of indexes of selected elements """        
        return self.bio_tags(self.p)

    def common_elements(self):
        """ -> set of indexes of common elements """
        return self.relevant_elements().\
               intersection(self.selected_elements())

    def true_positives(self):
        """ -> set of indexes of true positives """        
        return [i for i in self.common_elements()
                if self.c[i]==self.p[i]]
        
    def precision(self):
        """ -> precision value """
        return len(self.true_positives())*100/\
               len(self.selected_elements())

    def recall(self):
        """ -> recall value """
        return len(self.true_positives())*100/\
               len(self.relevant_elements())

    def f_measure(self,beta=1):
        """ -> f-measure value """
        pre = self.precision()
        rec = self.recall()
        alpha = 1/(1+beta*beta)
        return 1/(alpha/pre+(1-alpha)/rec)
                    
if __name__ == "__main__":
    c = 'B-What I-What O B-What B-What O O      B-Who O O'.split()
    p = 'B-What I-What O O      I-What O B-What B-Who O O'.split()
    m = Metrics_BIO(c,p)
    
    

    
