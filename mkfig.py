from enum import auto
from turtle import update
from sudachipy import tokenizer
from sudachipy import dictionary
from nltk.util import ngrams
from nltk import bleu_score
from collections import Counter
from fractions import Fraction
import time
import csv
import datetime
from tqdm import tqdm
import numpy as np
from statistics import mean
import matplotlib.pyplot as plt

def makeFig(array,data_name:str):
    plt.hist(array,bins=40)
    plt.title(str(data_name)+"'s function")
    dt_now = datetime.datetime.now()
    plt.savefig("./outputFig/"+str(data_name)+ dt_now.strftime('%y%m%d-%H%M%S'))
    plt.show()
    return None

def mkfig():
    '''
    図を作りたい
    '''
    str = input()
    with open('./outputCSV/'+str) as f:
        reader = csv.reader(f)
        inputArray = [row for row in reader]
    f.close()
    # outputArray = ['oitama', 'result', 'answer', 'fScore', 'bleuscore', 'option_result', 'fcore-option', 'option効果']
    
    arr = np.array(inputArray[1:-1]).transpose(1, 0)
    makeFig(arr[3],'fscore')
    makeFig(arr[6],'fscore-option')
    makeFig(arr[7],'option-effect')
    # print(arr[3],'fscore')
    # print(arr[6],'fscore-option')
    # print(arr[7],'option-effect')

if __name__ == '__main__':
    # 引数は何回、格助詞ランダムを実行して平均を取るか
    mkfig()