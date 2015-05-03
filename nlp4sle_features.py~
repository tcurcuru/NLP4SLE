# -*- coding: utf-8 -*-

"""
cosi140b - NLP4SLE - Machine Learning
Feature Extraction Module

Reference:
- http://nbviewer.ipython.org/github/tpeng/python-crfsuite/blob/master/examples/CoNLL%202002.ipynb

Demo:
>>> ================================ RESTART ================================
>>> 
Total feature extraction time: 0 seconds

Sample features:

bias w=Birthdays w.istitle=True pos=NNPS BOS nw=& nw.istitle=False npos=CC I-Ent_What_Topic

bias w=& w.istitle=False pos=CC pw=Birthdays pw.istitle=True ppos=NNPS nw=Anniversaries nw.istitle=True npos=NNPS I-Ent_What_Topic

bias w=Anniversaries w.istitle=True pos=NNPS pw=& pw.istitle=False ppos=CC nw=Anniversary nw.istitle=True npos=NN I-Ent_What_Topic

>>>
"""

from nlp4sle_utilities import *
import time

# Feature functions

# Extract features from data
def w2f(sents,i,j):
    """ -> list of features for a word """
    w = sents[i][j][0] #current word
    pos = sents[i][j][1] #POS of current word
    f = [        
        'bias', #non-contextual feature        
        'w=' + w, #current word        
        'w.istitle=%s' % w.istitle(), #first letter - capitalized
        'pos=' + pos, # POS tag
        ]
    if j>0:
        pw = sents[i][j-1][0] #previous word
        ppos = sents[i][j-1][1] #POS of previous word
        f.extend([            
            'pw=' + pw, # previous word            
            'pw.istitle=%s' % pw.istitle(), #first letter - capitalized
            'ppos=' + ppos, # POS tag
            ])
    else:        
        f.append('BOS') #first word of a sentence

    if j<len(sents[i])-1:
        nw = sents[i][j+1][0] #next word
        npos = sents[i][j+1][1] #POS of next word
        f.extend([            
            'nw=' + nw, # previous word
            'nw.istitle=%s' % nw.istitle(), #first letter - capitalized
            'npos=' + npos, #POS tag
            ])
    else:        
        f.append('EOS') # last word of a sentence

    #if j>1: ...
    #if j<len(sents[i])-2: ...
    #if j>0 and j<len(sents[i])-1: ...
    return f

def s2f(sents,i):
    """ Extract features from a sentence """
    return [w2f(sents,i,j) for j in range(len(sents[i]))]


def s2l(sents,i):
    """ Extract labels from a sentence for gold data """
    return [str(l) for _,_,l in sents[i]]

def s2w(sents,i):
    """ Extract words from a sentence """
    return [w for w,_,_ in sents[i]]

def d2f(sents):
    """ Extract features from a document """
    return [s2f(sents,i) for i in range(len(sents))]

def d2l(sents):
    """ Extract labels from a document """
    return [s2l(sents,i) for i in range(len(sents))]

def extract_features(data_dir,mode='train'):
    """
    -> extract features from a corpus/ dataset
    mode = 'train'/'decode'
    """
    files = get_files(data_dir)
    t0 = time.time()
    features = list()
    labels = list()
    for f in files:
        if mode=='train':
            sents = corpus_reader(f)
            labels.extend(d2l(sents))
        elif mode=='decode':
            sents = corpus_reader(f,tag='pos')
        else:
            print 'Invalid mode!'
            break
        features.extend(d2f(sents))       
    dt = time.time() - t0
    print 'Total feature extraction time: %d seconds' % dt
    return features,labels   
    
if __name__ == "__main__":
    data_dir = 'train'
    df,dl = extract_features(data_dir)
    save_data(df,'train_features.pkl')
    save_data(dl,'train_labels.pkl')
    lines = list()
    for sf,sl in zip(df,dl):
        for wf,wl in zip (sf,sl):
            lines.append(' '.join(wf)+' '+wl+'\n')            
    write_lines(lines,'train_features.txt')
    print '\nSample features:\n'
    for line in lines[:3]:
        print line
    
    
