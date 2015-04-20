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

PROJECT_PATH = os.getcwd()
DATA_PATH = os.path.join(PROJECT_PATH, "data")
GOLD_PATH = os.path.join(DATA_PATH, "gold")
RAW_PATH = os.path.join(DATA_PATH, "raw")

def strip_out_text():
    for f in os.listdir(GOLD_PATH):
        soup = bs(open( os.path.join(GOLD_PATH, f), "r", encoding='utf-8') )
        text = soup.get_text()
        with open( f[:-4] + '.txt', "w+", encoding='utf-8') as out_file:
            out_file.write(text)