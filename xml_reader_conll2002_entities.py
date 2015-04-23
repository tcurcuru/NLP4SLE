# -*- coding: utf-8 -*-

"""
This program is to:
Deal with XML files
"""

__author__ = ['TJC']
__date__ = "4/19/2015"
__email__ = ['tcurcuru@brandeis.edu']

import os
import glob
from bs4 import BeautifulSoup as bs
import codecs

PROJECT_PATH = os.getcwd()
DATA_PATH = os.path.join(PROJECT_PATH, "data")
GOLD_PATH = os.path.join(DATA_PATH, "gold")
PARSE_PATH = os.path.join(DATA_PATH, "parsed")

def strip_out_text():
    for f in os.listdir(GOLD_PATH):
        soup = bs(open( os.path.join(GOLD_PATH, f), "r", encoding='utf-8') )
        text = soup.get_text()
        with open( f[:-4] + '.txt', "w+", encoding='utf-8') as out_file:
            out_file.write(text)
            
#def remove_returns():
#    for f in os.listdir(RAW_PATH):
#        with open( os.path.join(RAW_PATH, f), "r", encoding='utf-8') as in_file:
#            text = "\n"
#            for line in in_file:
#                text += line.replace('\r', '')
#            with open(f[:-4] + "_fixed.txt", "w+", encoding='utf-8') as out_file:
#                out_file.write(text)
        
def create_gold_training_files():
    for f in os.listdir(GOLD_PATH):
        f_name = f[:-9]
        parse_f = f_name + ".fix.xml"
        #gold_soup = bs(open(os.path.join(GOLD_PATH, f), "r", encoding='utf-8'))
        #stan_soup = bs(open(os.path.join(PARSE_PATH, parse_f), "r", encoding='utf-8'))
        gold_soup = bs(codecs.open(os.path.join(GOLD_PATH, f), "r", encoding='utf-8'))
        stan_soup = bs(codecs.open(os.path.join(PARSE_PATH, parse_f), "r", encoding='utf-8'))
        
        gold_mentions = []
        for mention in gold_soup.findAll('entity_mention'):
            if mention['meta_type'] == 'Topic' or mention['meta_type'] == 'Sub-Topic':
                gold_mentions.append(mention)
        #gold_adverbials = []
        #for mention in gold_soup.findAll('adverbial'):
            #if mention['meta_type'] == 'Topic' or mention['meta_type'] == 'Sub-Topic':
                #gold_adverbials.append(mention)
                
        gold_spans = []
        for mention in gold_mentions:
            start, end = mention['spans'].split('~')
            #gold_spans.append( (start, end, "Ent_" + str(mention['type']) + "_" \
                                                   #+ str(mention['meta_type']) ))
            gold_spans.append( (start, end, str(mention['type']) + "_" \
                                          + str(mention['meta_type'])[0] ))
        #for mention in gold_adverbials:
            #start, end = mention['spans'].split('~')
            #gold_spans.append( (start, end, "Adv_" + str(mention['type']) + "_" \
                                                   #+ str(mention['meta_type']) ))
            
        #with open(f_name + "_gold", "w+", encoding='utf-8') as out_f:
        with codecs.open(f_name + "_gold_ent", "w+", encoding='utf-8') as out_f:
            for sent in stan_soup.findAll('sentence'):
                for token in sent.findAll('token'):
                    #begin = str(token.characteroffsetbegin)[22:-23]
                    #end = str(token.characteroffsetend)[20:-21]
                    begin = token.characteroffsetbegin.string
                    end = token.characteroffsetend.string
                    
                    #out_f.write(str(token.word)[6:-7] + '\t')   # word
                    out_f.write(token.word.string + '\t')
                    #out_f.write(sent['id'] + '\t')              # sent number
                    #out_f.write(token['id'] + '\t')             # pos in sent
                    #out_f.write(begin + '\t')                   # start offset
                    #out_f.write(end + '\t')                     # end offset
                    #out_f.write(str(token.pos)[5:-6] + '\t')    # POS tag
                    out_f.write(token.pos.string + '\t')
                    
                    out = True
                    for mention in gold_spans:
                        if int(begin) == int(mention[0]):
                            out_f.write("B-" + mention[2] + '\t')
                            out = False
                            break
                        if int(begin) > int(mention[0]) \
                        and int(end) <= int(mention[1]):
                            out_f.write("I-" + mention[2] + '\t')
                            out = False
                            break
                    if out:
                        out_f.write("O\t")
                        
                    out_f.write('\n')
                # empty line as sentence separation
                out_f.write('\n')
                    
create_gold_training_files()
