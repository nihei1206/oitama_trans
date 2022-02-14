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
import statistics
import math


def makeFig(array, data_name:str,bins:int,sub_name):
    
    median = statistics.median(array)
    ave = statistics.mean(array)
    plt.style.use('ggplot')
    plt.figure(figsize=(10, 10), dpi=40)
    plt.hist(array,bins=bins,range = (0,1), color="blue", edgecolor="black", linestyle="--",rwidth = 0.8)
    plt.title('Histogram of '+str(data_name) + str(sub_name), fontsize = 24,color = 'k') 
    plt.xticks(fontsize = 32,color = 'k', fontweight = 'bold')
    plt.xlabel("F-score", fontsize=24,color = 'k') 
    plt.ylabel("Frequency", fontsize=24,color = 'k')

    # if split
    # plt.yticks(np.arange(0, 65, 5),fontsize=32, fontweight = 'bold',color = 'k')
    # if trans
    plt.yticks(np.arange(0, 22, 2),fontsize=32, fontweight = 'bold',color = 'k')

    dt_now = datetime.datetime.now()
    plt.savefig("./outputFig/" +str(data_name) + str(sub_name)+ dt_now.strftime('%H%M%S'))
    plt.show()
    
    return "Done! " + str(data_name) + str(sub_name)+ ": median is " + str(median) +  " / Ave is " + str(ave)

def mkfig(dataname,dataType,bins):
    '''
    図を作りたい
    '''
    # with open('./outputCSV/0209_ver4/' + filename + "_result.csv") as f:
    with open("./outputCSV/0209_ver4/"+ str(dataname) + "_result.csv") as f:
        reader = csv.reader(f)
        inputArray = [row for row in reader]
    f.close()

    inputArray = np.array(inputArray[1:-1])

    if dataType == 'split' or  dataType == 's':
        floatArray = np.array(inputArray.transpose(1, 0)[4],dtype = np.float64)
        print(makeFig(floatArray,dataname,bins,''))
    elif dataType == 'trans' or  dataType == 't':
        floatArray = np.array(inputArray.transpose(1, 0)[3],dtype = np.float64)
        print(makeFig(floatArray,dataname,bins,''))

        floatArray = np.array(inputArray.transpose(1, 0)[6],dtype = np.float64)
        print(makeFig(floatArray,dataname,bins,'-option'))

if __name__ == '__main__':
    print('split(s) or trans(t)')
    dataType = str(input())

    if dataType == 'split' or dataType == 's':
        print('Oitama or Sudachi')
        dataname = str(input())
    elif dataType == 'trans' or dataType == 't':
        dataname = str('Translator')
    print('input bins')
    bins = int(input())
    mkfig(dataname,dataType,bins)