from sudachipy import tokenizer
from sudachipy import dictionary
from collections import Counter
from fractions import Fraction
import time
import csv
import datetime
from tqdm import tqdm
import numpy as np
import option as op

### Initialized Takenizer ### 
# トークナイザの作成,辞書位置(sudachi.json ; 相対パス)の指定
# Qsudachidict_full優先 dict="full"

def replacement(text:str,tokenizer_obj:tokenizer.Tokenizer,option:int):
    '''
    #入力された文章を,SudachiDictとUserDictで翻訳
    '''
    #ユーザー辞書のパスを宣言
    config_path_link = "./lib/python3.9/site-packages/sudachipy/resources/sudachi.json"
    #ユーザー辞書の使用を宣言
    tokenizer_obj = dictionary.Dictionary(config_path=config_path_link).create() 
    mode = tokenizer.Tokenizer.SplitMode.C
    combinedExchangeHogen = []
    tokens = tokenizer_obj.tokenize(text,mode)
    for m in tokens:
        if m.part_of_speech()[5] == '方言':
            combinedExchangeHogen.append(m.normalized_form())
        else:
            combinedExchangeHogen.append(m.surface())
    
    if option == 0:
        combinedExchangeHogentext = "".join(combinedExchangeHogen)
        return combinedExchangeHogentext
    if option == 1:
        #欠落の格助詞補完
        translatedOutput = op.addDropedWord(combinedExchangeHogentext)
        return translatedOutput