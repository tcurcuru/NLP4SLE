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

from __future__ import print_function
from bs4 import BeautifulSoup as bs
from nlp4sle_utilities import *
import time
import os
#import sys
import codecs
from nltk.corpus import stopwords

#reload(sys)
#sys.setdefaultencoding('utf8')

HOME = os.getcwd()
DATA = os.path.join(HOME, "data")
FIXED = os.path.join(DATA, "fixed")
PARSED = os.path.join(DATA, "parsed")

def get_frequencies(filename):
    """Calculates frequencies for all words in a document"""
    freq_dict = {}
    _,long_name = filename.split("\\")
    name,_ = long_name.split("_gold_")
    f = os.path.join(PARSED, name + ".fix.xml")
    #soup = bs(open(f, 'r'))
    soup = bs(codecs.open(f, 'r', encoding='utf-8'))
    for sent in soup.findAll('sentence'):
        for token in sent.findAll('token'):
            try:
                w = token.word.string
                if w in freq_dict:
                    freq_dict[w] += 1
                else:
                    freq_dict[w] = 1
            except AttributeError:
                pass
    return freq_dict

# Stop Word List from NLTK
swl = stopwords.words()
def stop_word(w):               # local feature
    """ -> True if w is a stop word """
    return (w in swl)
    
# Feature functions
def get_title(filename):
    """Gets the title aka first line from a file"""
    _,long_name = filename.split("\\")
    name,_ = long_name.split("_gold_")
    f = os.path.join(FIXED, name + ".fix")
    #with open(f, 'r') as in_f:
    with codecs.open(f, 'r', encoding='utf-8') as in_f:
        lines = in_f.readlines()
        i = 0
        line = lines[i]
        while len(line) < 5:
            i += 1
            line = lines[i]
        return lines[i]
        
def contained_in_title(word, filename):
    """Checks if a word is contained in the title of a document"""
    title = get_title(filename)
    if word in title:
        return True
    else:
        return False
        
def lower_in_title(word, filename):
    """Checks if a word is contained in the title of a document, but both lower-
    cased"""
    title = get_title(filename)
    if word.lower() in title.lower():
        return True
    else:
        return False
        
def frequency(word, freq):
    """Checks if the word is a high frequency word in the document"""
    if word in freq:
        if freq[word] > 2:
            return 'high'
        else:
            return 'low'
    else:
        return 'none'
            
# Extract features from data
def w2f(sents,i,j,filename,freq):
    """ -> list of features for a word """
    w = sents[i][j][0] #current word
    pos = sents[i][j][1] #POS of current word
    f = [        
        'bias', #non-contextual feature        
        'w=' + w, #current word        
        'w.istitle=%s' % w.istitle(), #first letter - capitalized
        'pos=' + pos, # POS tag
        'w.intitle=%s' % contained_in_title(w, filename), # w matches title
        'w.lowtitle=%s' % lower_in_title(w, filename), # w lower matches title
        'w.freq=%s' % frequency(w, freq), # freq of w        
        'w.stopword=%s' % stop_word(w), # # stop word
        ]
        
    # previous word features
    if j>0:
        pw = sents[i][j-1][0] #previous word
        ppos = sents[i][j-1][1] #POS of previous word
        f.extend([            
            'pw=' + pw, # previous word            
            'pw.istitle=%s' % pw.istitle(), #first letter - capitalized
            'ppos=' + ppos, # POS tag
            'pw.intitle=%s' % contained_in_title(pw, filename), # w matches title
            'pw.lowtitle=%s' % lower_in_title(pw,filename), # w lower matches title
            'pw.freq=%s' % frequency(pw, freq), # freq of w
            'pw.stopword=%s' % stop_word(w), # # stop word
            ])
    else:        
        f.append('BOS') #first word of a sentence

    # next word features
    if j<len(sents[i])-1:
        nw = sents[i][j+1][0] #next word
        npos = sents[i][j+1][1] #POS of next word
        f.extend([            
            'nw=' + nw, # previous word
            'nw.istitle=%s' % nw.istitle(), #first letter - capitalized
            'npos=' + npos, #POS tag
            'nw.intitle=%s' % contained_in_title(nw, filename), # w matches title
            'nw.lowtitle=%s' % lower_in_title(nw,filename), # w lower matches title
            'nw.freq=%s' % frequency(nw, freq), # freq of w
            'nw.stopword=%s' % stop_word(w), # # stop word
            ])
    else:        
        f.append('EOS') # last word of a sentence

    #if j>1: ...
    #if j<len(sents[i])-2: ...
    #if j>0 and j<len(sents[i])-1: ...
    return f

def s2f(sents,i,f,freq):
    """ Extract features from a sentence """
    return [w2f(sents,i,j,f,freq) for j in range(len(sents[i]))]


def s2l(sents,i,f,freq):
    """ Extract labels from a sentence for gold data """
    return [str(l) for _,_,l in sents[i]]

def s2w(sents,i,f,freq):
    """ Extract words from a sentence """
    return [w for w,_,_ in sents[i]]

def d2f(sents,f,freq):
    """ Extract features from a document """
    return [s2f(sents,i,f,freq) for i in range(len(sents))]

def d2l(sents,f,freq):
    """ Extract labels from a document """
    return [s2l(sents,i,f,freq) for i in range(len(sents))]

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
        freq = get_frequencies(f)
        if mode=='train':
            sents = corpus_reader(f)
            labels.extend(d2l(sents,f,freq))
        elif mode=='decode':
            sents = corpus_reader(f,tag='pos')
        else:
            print('Invalid mode!')
            break
        features.extend(d2f(sents,f,freq))       
    dt = time.time() - t0
    print('Total feature extraction time: %d seconds' % dt)
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
    print('\nSample features:\n')
    for line in lines[:3]:
        print(line)
    
    
