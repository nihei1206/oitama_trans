from sudachipy import tokenizer
from sudachipy import dictionary
import random
from statistics import mean
from hyoka import hyoka_trans as ht

def addDropedWord(text:str) -> str:
    '''
    欠落語補完機能
    名詞,形容詞が連続した場合,間に「が」を入れることで「が」の欠落を補完
    名詞,動詞が連続した場合,間に「に」を入れることで「に(さ)」の欠落を補完
    仮説 ->「さ」助詞を補完したらなんでもうまく行くのではないか
    口語文書の解析精度向上のための 助詞落ち推定および補完 ...の論文より割合を引用
    default = {'が':15.2,'を':16.7,'に':0.7,'で':1.4,'の':1.5,'は':31.5,'と':33.0}
    置賜カスタマイズ(「山形県のことば」より、省略される助詞と明記されているもののみを実行)
    yamagata custom = {'が':23.42,'を':25.73,'の':2.31,'は':48.53} ->4kjs
    {'が':71.95,'を':25.73,'の':2.32} -> 3kjs

    '''
    config_path_link = "./lib/python3.9/site-packages/sudachipy/resources/sudachi.json"
    tokenizer_obj = dictionary.Dictionary(config_path=config_path_link).create() 
    mode = tokenizer.Tokenizer.SplitMode.C
    tokens = tokenizer_obj.tokenize(text,mode)
    wordPartofspeech = []
    wordCombine = []
    kakujoshi_dict = {'が':1,'を':1,'に':1}
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

def manytimeFscore(text1:str,text2:str,n:int):
    '''
    何度もランダム格助詞補完法を実施し、その平均を取る
    一番精度が高かった値をreturn
    '''
    arr = []
    for k in range(1,n+1):
        if not ht.translate_hyoka(text1,text2,1)[3] == None:
            arr.append(ht.translate_hyoka(text1,text2,1)[3])
    max_ = [i for i, v in enumerate(arr) if v == max(arr)]
    maxtimesIndex = int(mean(max_))
    maxArr = float(max(arr))
    return maxArr,maxtimesIndex