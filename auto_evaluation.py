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
import random

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

    #欠落の[が]補完
    translatedOutput = addDropedWord(combinedExchangeHogentext)

    return translatedOutput

def addDropedWord(text:str) -> str:
    '''
    欠落語補完機能
    名詞,形容詞が連続した場合,間に「が」を入れることで「が」の欠落を補完
    名詞,動詞が連続した場合,間に「に」を入れることで「に(さ)」の欠落を補完
    仮説 ->「さ」助詞を補完したらなんでもうまく行くのではないか

    作戦:頻繁に使われる動詞と形容詞をすべて抽出し、直前につくであろう格助詞情報を付与する。
    配列の中に、surface,partOfSpeech,seikika情報を格納し、条件マッチで任意の格助詞に置換
    分割->sudachiDict正規化->直前に格助詞を配置-> 
    user_dict(格助詞)に参照してreturn(は、へ、を、が、に、null)の関数を作る必要がありそう?
    key,value置換で良くない？
    '''
    mode = tokenizer.Tokenizer.SplitMode.C
    tokens = tokenizer_obj.tokenize(text,mode)
    wordPartofspeech = []
    wordCombine = []
    kakujoshi_dict = {'に':1,'へ':1,'が':2,'を':3}
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
    print(wordPartofspeech)
    return wordOutput

print(addDropedWord('喉乾いだー'))

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

def translate_hyoka(oitama:str, answer:str) -> list:
    '''
    #return [answer:str,oitama:str,result:str,fScore:float,bleuScore:float]
    '''
    #置賜弁をここで標準語に翻訳
    config_path_link = "lib/python3.9/site-packages/sudachipy/resources/sudachi.json"
    tokenizer_obj = dictionary.Dictionary(config_path=config_path_link,dict="full").create() 
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
        fScore = None
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
            # if not (inputArray[i][0] and inputArray[i][1]):
            #     outputArray.append(['No.'+str(i+1)+' is skeped'])
            # else:
            outputArray.append(translate_hyoka(inputArray[i][1],inputArray[i][0]))
                
        header = ['oitama','result','answer','fScore','bleuScore']
        dt_now = datetime.datetime.now()
        with open('./outputCSV/OitamaTrans'+ dt_now.strftime('%y%m%d-%H%M%S') +'.csv', 'w') as f:
 
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(outputArray)

        f.close()
        elapsed_time = time.time() - start

        return print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

# importArrayfromCSV_then_do()

