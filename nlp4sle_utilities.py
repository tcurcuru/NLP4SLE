# -*- coding: utf-8 -*-

"""
cosi140b - NLP4SLE - Machine Learning
Utilities Module

Corpus Demo:
>>> ================================ RESTART ================================
>>> 
Please enter your corpus path (example: name_gold_pruned):
train/nlp4sle_holidays_asian_gold_pruned
tag = bio
>>> corpus[0]
[(u'Asian', u'NNP', u'B-Ent_What_Topic'), (u'Pacific', u'NNP', u'I-Ent_What_Topic'), (u'American', u'NNP', u'I-Ent_What_Topic'), (u'Heritage', u'NNP', u'I-Ent_What_Topic'), (u'Month', u'NNP', u'I-Ent_What_Topic'), (u'May', u'NNP', u'B-Ent_What_Topic'), (u'Much', u'RB', u'O'), (u'like', u'IN', u'O'), (u'Black', u'JJ', u'O'), (u'History', u'NN', u'O'), (u'Month', u'NNP', u'O'), (u'and', u'CC', u'O'), (u'Women', u'NNP', u'O'), (u"'s", u'POS', u'O'), (u'History', u'NN', u'O'), (u'Month', u'NNP', u'O'), (u',', u',', u'O'), (u'Asian', u'NNP', u'B-Ent_What_Topic'), (u'Pacific', u'NNP', u'I-Ent_What_Topic'), (u'American', u'NNP', u'I-Ent_What_Topic'), (u'Heritage', u'NNP', u'I-Ent_What_Topic'), (u'Month', u'NNP', u'I-Ent_What_Topic'), (u'originated', u'VBD', u'O'), (u'with', u'IN', u'O'), (u'a', u'DT', u'O'), (u'congressional', u'JJ', u'B-Ent_What_Sub-Topic'), (u'bill', u'NN', u'I-Ent_What_Sub-Topic'), (u'.', u'.', u'O')]
>>> ================================ RESTART ================================
>>> 
Please enter your corpus path (example: name_gold_pruned):
train/nlp4sle_holidays_asian_gold_pruned
tag = pos
>>> corpus[0]
[(u'Asian', u'NNP'), (u'Pacific', u'NNP'), (u'American', u'NNP'), (u'Heritage', u'NNP'), (u'Month', u'NNP'), (u'May', u'NNP'), (u'Much', u'RB'), (u'like', u'IN'), (u'Black', u'JJ'), (u'History', u'NN'), (u'Month', u'NNP'), (u'and', u'CC'), (u'Women', u'NNP'), (u"'s", u'POS'), (u'History', u'NN'), (u'Month', u'NNP'), (u',', u','), (u'Asian', u'NNP'), (u'Pacific', u'NNP'), (u'American', u'NNP'), (u'Heritage', u'NNP'), (u'Month', u'NNP'), (u'originated', u'VBD'), (u'with', u'IN'), (u'a', u'DT'), (u'congressional', u'JJ'), (u'bill', u'NN'), (u'.', u'.')]
>>>
"""

from __future__ import with_statement,print_function
import os
from cPickle import dump, load, HIGHEST_PROTOCOL
from nltk.corpus import conll2002 as reader
import codecs

def read_lines(data_file):
    """ data file -> lines (strings) """
    with codecs.open(data_file,'r',encoding='utf-8') as f:
        for line in f.readlines():
            yield line

def write_lines(lines,data_file):
    """ lines -> data file """
    with codecs.open(data_file,'w',encoding='utf-8') as f:
        for line in lines:
            f.write(line)

def get_files(directory):
    """ -> list of file names in a directory """
    output = list()
    for root,dirs,files in os.walk(directory):
        output.extend(os.path.join(root,f) for f in files)
    return sorted(output)

def save_data(data,pklfile_name):
    """ save data to a pickle file """        
    with open(pklfile_name,'wb') as f:
        dump(data,f,HIGHEST_PROTOCOL)

def load_data(pklfile_name):
    """ load data from a pickle file """        
    with open(pklfile_name,'rb') as f:
        data = load(f)
    return data

def corpus_reader(corpus_path,tag='bio'):
    """ corpus relative path (str) -> list of iob sents """
    if tag=='bio':  # training dataset
        return reader.iob_sents(os.path.abspath(corpus_path))
    if tag=='pos':  # test dataset
        return reader.tagged_sents(os.path.abspath(corpus_path))
    
def get_corpus_path():
    """ Interactive function to get corpus path """
    corpus_path = raw_input\
                  ("Please enter your corpus path " +
                   "(example: name_gold_pruned):\n")
    if os.access(corpus_path,os.F_OK):
        return corpus_path
    else:
        print('This path does not exist.\n')
        return get_corpus_path()
                    
if __name__ == "__main__":
    corpus = corpus_reader(get_corpus_path(),\
                           tag=raw_input('tag = '))
