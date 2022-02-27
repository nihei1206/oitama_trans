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
from statistics import mean

def sudachionlyWakachi(text:str) -> list:
    '''
    sudachi_dictだけでの分割
    '''
    hyokaArrayonly = []
    mode = tokenizer.Tokenizer.SplitMode.A
    config_path_link = "lib/python3.9/site-packages/sudachipy/resources/notuse_resources/sudachi.json"
    tokenizer_obj = dictionary.Dictionary(config_path=config_path_link,dict="full").create()
    tokens = tokenizer_obj.tokenize(text,mode)
    for m in tokens:
        hyokaArrayonly.append(m.surface())
    return hyokaArrayonly

def sudachiOitamaWakachi(text:str) -> list:
    '''
    sudachi_dictとOitama_dictでの分割
    '''
    outputArray = []
    mode = tokenizer.Tokenizer.SplitMode.A
    config_path_link = "lib/python3.9/site-packages/sudachipy/resources/sudachi.json"
    tokenizer_obj = dictionary.Dictionary(config_path=config_path_link,dict="full").create()
    tokens = tokenizer_obj.tokenize(text,mode)
    for m in tokens:
        outputArray.append(m.surface())
    return outputArray

def hyoka(result:list,answer:list) -> list:
    '''
    fig.8-1:
    return result,answer,precision,recall,Fscore
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

    if precision == 0 and recall == 0:
        return result,answer,precision ,recall ,0
    else:
        Fscore = (2 * precision * recall) / ( precision + recall )
        # return result,answer,precision,recall,Fscore
        return result,answer,precision ,recall ,Fscore

def canmaBunkatsu(text:str) -> list:
    '''
    ,分割
    '''
    outputArray = text.split(',')
    return outputArray

def average(array:list) -> list:
    seido_arr = []
    saigen_arr = []
    fscore_arr = []

    for i in range(len(array)):
        seido_arr.append(array[i][2])
        saigen_arr.append(array[i][3])
        fscore_arr.append(array[i][4])
    seido_ave = mean(seido_arr)
    saigen_ave = mean(saigen_arr)
    f_ave = mean(fscore_arr)
    return '平均',None,seido_ave,saigen_ave,f_ave

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
        for i in tqdm(range(1,len(inputArray))):
            np.pi*np.pi
            outputArray.append(hyoka(sudachiOitamaWakachi(inputArray[i][1]),canmaBunkatsu(inputArray[i][2])))
        
        outputArray.append(average(outputArray))

        header = ['result','answer','seido','saigen','Fscore']
        dt_now = datetime.datetime.now()
        with open('./outputCSV/Bunkatsu_OitamaDict'+ dt_now.strftime('%y%m%d-%H%M%S') +'.csv', 'w') as f:
 
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(outputArray)

        f.close()
        
        outputArray = []
        for i in tqdm(range(1,len(inputArray))):
            np.pi*np.pi
            outputArray.append(hyoka(sudachionlyWakachi(inputArray[i][1]),canmaBunkatsu(inputArray[i][2])))

        outputArray.append(average(outputArray))
        header = ['result','answer','seido','saigen','Fscore']
        dt_now = datetime.datetime.now()
        with open('./outputCSV/Bunkatsu_sudachiDict'+ dt_now.strftime('%y%m%d-%H%M%S') +'.csv', 'w') as f:
 
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(outputArray)

        f.close()
        elapsed_time = time.time() - start

        return print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

if __name__ == '__main__':
    importArrayfromCSV_then_do()