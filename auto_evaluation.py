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
import numpy
import random
import statistics
from statistics import mean
import matplotlib.pyplot as plt

### Initialized Takenizer ### 
# トークナイザの作成,辞書位置(sudachi.json ; 相対パス)の指定
# Qsudachidict_full優先 dict="full"
# mode(a,b,c)の指定
config_path_link = "lib/python3.9/site-packages/sudachipy/resources/sudachi.json"
#ユーザー辞書の使用を宣言
tokenizer_obj = dictionary.Dictionary(config_path=config_path_link).create() 
mode = tokenizer.Tokenizer.SplitMode.C

def translaterOitama(text:str,tokenizer_obj:tokenizer.Tokenizer) -> str:
    '''
    #入力された文章を,SudachiDictとUserDictで翻訳
    #今後ここの中の任意の場所に高度な例外処理を組み込みたい
    #splitMode == C
    '''
    mode = tokenizer.Tokenizer.SplitMode.C
    combinedExchangeHogen = []
    tokens = tokenizer_obj.tokenize(text,mode)
    for m in tokens:
        if m.part_of_speech()[5] == '方言':
            combinedExchangeHogen.append(m.normalized_form())
        else:
            combinedExchangeHogen.append(m.surface())
    combinedExchangeHogentext = "".join(combinedExchangeHogen)
    return combinedExchangeHogentext

def translaterOitamaOption(text:str,tokenizer_obj:tokenizer.Tokenizer) -> str:
    '''
    #入力された文章を,SudachiDictとUserDictで翻訳
    #今後ここの中の任意の場所に高度な例外処理を組み込みたい
    #splitMode == C
    '''
    mode = tokenizer.Tokenizer.SplitMode.C
    combinedExchangeHogen = []
    tokens = tokenizer_obj.tokenize(text,mode)
    for m in tokens:
        if m.part_of_speech()[5] == '方言':
            combinedExchangeHogen.append(m.normalized_form())
        else:
            combinedExchangeHogen.append(m.surface())
    combinedExchangeHogentext = "".join(combinedExchangeHogen)

    #欠落の格助詞補完
    translatedOutput = addDropedWord(combinedExchangeHogentext)

    return translatedOutput

def noukinTrans(text:str) -> str:
    '''
    脳筋翻訳機能
    仮説 -> 標準語ではない単語の場合、その単語の濁音・促音の有無を全種類試行することで
    いい感じになるのではないか。これが役に立つのはど田舎と都会の中間地点の方言地域に限られると思う
    '''

    return

def addDropedWord(text:str) -> str:
    '''
    欠落語補完機能
    名詞,形容詞が連続した場合,間に「が」を入れることで「が」の欠落を補完
    名詞,動詞が連続した場合,間に「に」を入れることで「に(さ)」の欠落を補完
    仮説 ->「さ」助詞を補完したらなんでもうまく行くのではないか
    口語文書の解析精度向上のための 助詞落ち推定および補完 ...の論文より割合を引用
    default = {'が':15.2,'を':16.7,'に':0.7,'で':1.4,'の':1.5,'は':31.5,'と':33.0}
    置賜カスタマイズ(「山形県のことば」より、省略される助詞と明記されているもののみを実行)
    yamagata custom = {'が':23.42,'を':25.73,'の':2.31,'は':48.53}
    '''
    mode = tokenizer.Tokenizer.SplitMode.C
    tokens = tokenizer_obj.tokenize(text,mode)
    wordPartofspeech = []
    wordCombine = []
    kakujoshi_dict = {'が':23.42,'を':25.73,'の':2.31,'は':48.53}
    candidates = [*kakujoshi_dict]
    weights = [*kakujoshi_dict.values()]
    randomed_kakujoshi = random.choices(candidates, weights=weights)[0]
    for m in tokens:
        wordPartofspeech.append([m.surface(),m.part_of_speech()[0]])        

    for j in range(len(wordPartofspeech)-1):
        if wordPartofspeech[j][1] == '名詞' or wordPartofspeech[j][1] == '代名詞':
            if wordPartofspeech[j+1][1] == '動詞' or wordPartofspeech[j+1][1] == '形容詞':
                wordPartofspeech.insert(j+1,[randomed_kakujoshi,'助詞',''])

    for k in range(len(wordPartofspeech)):
        wordCombine.append(wordPartofspeech[k][0])
    wordOutput = "".join(wordCombine)
    return wordOutput

def hyokaArray_trans(text:str,tokenizer_obj:tokenizer.Tokenizer) -> list:
    '''
    #入力された文章を,評価するための配列にsudachidictのみでわかち書き
    #splitMode == A
    '''
    hyokaArray = []
    mode = tokenizer.Tokenizer.SplitMode.A
    tokens = tokenizer_obj.tokenize(text,mode)
    for m in tokens:
        hyokaArray.append(m.surface()+str(m.part_of_speech()))
    return hyokaArray

def wakachiWrite(text:str,tokenizer_obj:tokenizer.Tokenizer) -> list:
    '''
    #文章を入力し単純にsudachidictでわかち書き
    #splitMode == A    
    '''
    #print(type(text), type(tokenizer_obj))
    mode = tokenizer.Tokenizer.SplitMode.A
    tokens = tokenizer_obj.tokenize(text,mode)
    wakachi_Array = []
    for m in tokens:
        wakachi_Array.append(m.surface())
    return wakachi_Array

def transOitamaToJp_inclde_info(text:str,tokenizer_obj:tokenizer.Tokenizer) -> list:
    '''
    #入力された文章を:方言,:標準語情報込みでわかち書きをして配列で出力する関数->出力確認用使わない
    #splitMode == A  
    '''
    hogenOrNotArray = []
    mode = tokenizer.Tokenizer.SplitMode.C
    tokens = tokenizer_obj.tokenize(text,mode)
    for m in tokens:
        if m.part_of_speech()[5] == '方言':
            hogenOrNotArray.append(m.surface()+':方言->'+m.normalized_form()+':標準語')
        else:
            hogenOrNotArray.append(m.surface()+':標準語')
    return hogenOrNotArray

def list_difference(list1:list, list2:list) -> list:
    '''
    #配列差分出力関数
    #list1にあって、list2にない要素を出力
    #list1に重複{2つ同じ要素}があったら、2つとカウント。
    #list2に同一要素が1つだとしたら、1つだけ出力される
    '''
    result = list1.copy()
    for value in list2:
        if value in result:
            result.remove(value)
    return result

def translate_hyoka(oitama:str, answer:str , hyokaOption:int) -> list:
    '''
    hyokaOption == 0 ->置換のみ手法
    hyokaOption == 1 -> 脳筋Option(格助詞の確立的はめ込み)
    #return [answer:str,oitama:str,result:str,fScore:float,bleuScore:float]
    '''
    #置賜弁をここで標準語に翻訳
    config_path_link = "lib/python3.9/site-packages/sudachipy/resources/sudachi.json"
    tokenizer_obj = dictionary.Dictionary(config_path=config_path_link,dict="full").create()
    
    if hyokaOption == 1:
        result = translaterOitamaOption(oitama,tokenizer_obj)
    else:
        result = translaterOitama(oitama,tokenizer_obj)

    # 変換後なので,ここからuserDictの不使用 => sudachiDict(full)のみの使用を宣言
    # config_path_link = "lib/python3.9/site-packages/sudachipy/resources/notuse_resources/sudachi.json"
    tokenizer_obj = dictionary.Dictionary(dict="full").create() 
    #Sudachidict_full優先 dict="full"

    #result:置賜弁を翻訳した結果
    #answer:用意している正解データ
    resultHyokaArray = hyokaArray_trans(result,tokenizer_obj)
    answerHyokaArray = hyokaArray_trans(answer,tokenizer_obj)

    # 正解データをわかち書き
    # 正解文を形態要素解析した正解配列と翻訳したあとの文を形態要素解析した配列を比較して、
    # 正解分にしかない配列の要素を配列にして出力したのがOnly_answer_list_have
    Only_answer_list_have = list_difference(answerHyokaArray,resultHyokaArray)
    system_output_word_count = len(resultHyokaArray) #翻訳した結果の全単語数
    answer_output_word_count = len(answerHyokaArray) #対応する正解データの全単語数
    correct_output_word_count = answer_output_word_count-len(Only_answer_list_have)
    seido = correct_output_word_count/system_output_word_count
    saigen = correct_output_word_count/answer_output_word_count

    ### Output ###
    # F-score
    # print("-- F score --")
    # print((2*seido*saigen)/(seido+saigen))
    if seido+saigen == 0:
        fScore = 0
    else:
        fScore = (2*seido*saigen)/(seido+saigen)

    # BLEU-score used option mothod7 (smoothing Function)
    # print("-- BLEU score --")
    # print(bleu_score.sentence_bleu([resultHyokaArray],answerHyokaArray,smoothing_function=bleu_score.SmoothingFunction().method7))
    # weights = (1./5., 1./5., 1./5., 1./5., 1./5.)
    # ngramの重み->weights これは連続するtokenの比較を行うんだけど、そのn連続という意味
    bleuScore = bleu_score.sentence_bleu([resultHyokaArray],answerHyokaArray,smoothing_function=bleu_score.SmoothingFunction().method7)

    if bleuScore == 0:
        bleuScore = None
    # input = (oitama:str , answer:str)

    return [oitama,result,answer,fScore,bleuScore]

def manytimeFscore(text1:str,text2:str,n:int) -> float:
    average = 0
    for i in range(1,n+1):
        sum = 0
        if not translate_hyoka(text1,text2,1)[3] == None:
            sum += float(translate_hyoka(text1,text2,1)[3])
        average = sum/n
    return average

def importArrayfromCSV_then_do(n_time):
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
        # for i in tqdm(range(100,120)):
            np.pi*np.pi
            adMF = translate_hyoka(inputArray[i][1],inputArray[i][0],0)
            adMF.append(manytimeFscore(inputArray[i][1],inputArray[i][0],n_time))
            outputArray.append(adMF)
        # print(outputArray[1])

        header = ['oitama','result','answer','fScore','bleuscore','fcore-hokan']
        dt_now = datetime.datetime.now()
        with open('./outputCSV/OitamaTrans'+ dt_now.strftime('%y%m%d-%H%M%S') +'.csv', 'w') as f:
 
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(outputArray)

        f.close()
        elapsed_time = time.time() - start

        return print("elapsed_time:{0}".format(elapsed_time) + "[sec]")


if __name__ == '__main__':
    importArrayfromCSV_then_do(30)

