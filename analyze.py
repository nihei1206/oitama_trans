import time
import csv
import pprint
import datetime
from tqdm import tqdm
import numpy as np
import math
import sys
import warnings

def analyzeCSV():
    '''
    # csvのimportからcsvのoutputまでやりたい処理をすべて詰め込みました
    # 実行時間の確認もできます
    '''

    start = time.time()
    with open('./auto_evaluation.csv') as f:
        reader = csv.reader(f)
        header = ['oitama','result','answer','fScore','bleuScore']
        dt_now = datetime.datetime.now()
        with open('OitamaOutput' + dt_now.strftime('%y%m%d-%H%M%S') +'.csv', 'w') as f:
 
            writer = csv.writer(f)

        f.close()
        elapsed_time = time.time() - start

        return print("elapsed_time:{0}".format(elapsed_time) + "[sec]")