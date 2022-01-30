import re
from turtle import update
from sudachipy import tokenizer
from sudachipy import dictionary
from nltk.util import ngrams
from nltk import bleu_score
import collections
import copy
import math
import sys
import warnings
from collections import Counter
from fractions import Fraction
import time
import csv
import pprint
import datetime
from tqdm import tqdm
import numpy as np

def sudachionlyWakachi(text) -> list:
    hyokaArrayonly = []
    mode = tokenizer.Tokenizer.SplitMode.A
    config_path_link = "lib/python3.9/site-packages/sudachipy/resources/notuse_resources/sudachi.json"
    tokenizer_obj = dictionary.Dictionary(config_path=config_path_link,dict="full").create()
    tokens = tokenizer_obj.tokenize(text,mode)
    for m in tokens:
        hyokaArrayonly.append(m.surface())
    return hyokaArrayonly

def sudachiOitamaWakachi(text) -> list:
    '''
    sudachi_dictとOitama_dictでの分割
    '''
    hyokaArray = []
    mode = tokenizer.Tokenizer.SplitMode.A
    # config_path_link = "lib/python3.9/site-packages/sudachipy/resources/sudachi.json"
    tokenizer_obj = dictionary.Dictionary(dict="full").create()
    tokens = tokenizer_obj.tokenize(text,mode)
    for m in tokens:
        hyokaArray.append(m.surface())
    return hyokaArray

oitama = 'いだくてがまんさんにぇ'
result_sudachi_dic = sudachionlyWakachi(oitama)
result_sudachi_oitama_dic = sudachiOitamaWakachi(oitama)
answerArray =['いだく','て','がまん','さん','にぇ']
print(result_sudachi_dic)
print(result_sudachi_oitama_dic)
print(answerArray)

# result = ['いだい', 'がら', 'しっ', 'ぷ', 'だし', 'て','けん','にぇ','が']
# resultはsudachi_dictとOitama_dictでの分割
# answer = ['いだい', 'がら', 'しっぷ', 'だし', 'て', 'けんにぇ','が']
# answerは人力分割
# only_sudachi_dic = ['いだい','がら','しっ','ぷ','だし','て','けん','に','ぇ','が']
# only_sudachi_dicはsudachi_dictのみでの分割

# print(answerArray)

# result = ['今日','も','し','ない','とね']
# answer = ['今日','もし','ない','と','ね']
#足が痛くてそんなことできない
#あしいだくてそげなごとさんにぇなー

# んじゃらば、車いすさ移んぞ。
# ['んじゃらば','、','車いす','さ','移ん','ぞ']

def hyoka(result:list,answer:list) -> list:
    '''
    fig.8-1:
    '''
    correct = 0
    result_index = 0
    answer_index = 0
    result_pos = 0
    answer_pos = 0

    while result_index < len(result) and answer_index < len(answer):
        if result_pos == answer_pos:
            if result[result_index] == answer[answer_index]:
                correct += 1
            result_pos += len(result[result_index])
            answer_pos += len(answer[answer_index])
            result_index += 1
            answer_index += 1
        
        elif result_pos > answer_pos:
            answer_pos += len(answer[answer_index])
            answer_index += 1
            
        elif result_pos < answer_pos:
            result_pos += len(result[result_index])
            result_index += 1

    precision = correct / len(result)
    recall = correct / len(answer)

    if int(precision) and int(recall) == 0:
        return None
    else:
        Fscore = (2 * precision * recall) / ( precision + recall )
        return precision ,recall ,Fscore

    # return result,answer,precision,recall,Fscore

print(hyoka(result_sudachi_dic,answerArray))
print(hyoka(result_sudachi_oitama_dic,answerArray))

def importArrayfromCSV_then_do() -> str:
    '''
    #csvのimportからcsvのoutputまでやりたい処理をすべて詰め込みました
    #実行時間の確認もできます
    '''

    start = time.time()
    with open('./auto_evaluation.csv') as f:
        reader = csv.reader(f)
        inputArray = [row for row in reader]
        outputArray = []
        # for i in tqdm(range(len(inputArray))):
        #     np.pi*np.pi
        #     if not (inputArray[i][0] and inputArray[i][1]):
        #         outputArray.append(['No.'+str(i+1)+' is skeped'])
        #     else:
        #         outputArray.append(translate_hyoka(inputArray[i][1],inputArray[i][0]))
                
        header = ['result','answer','seido','saigen','Fscore']
        dt_now = datetime.datetime.now()
        with open('OitamaOutput'+ dt_now.strftime('%y%m%d-%H%M%S') +'.csv', 'w') as f:
 
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(outputArray)

        f.close()
        elapsed_time = time.time() - start

        return print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

