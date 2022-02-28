from sudachipy import tokenizer as t
from sudachipy import dictionary as d
import option as op

### Initialized Takenizer ### 
# トークナイザの作成,辞書位置(sudachi.json ; 相対パス)の指定
# Qsudachidict_full優先 dict="full"

def replacement(text:str,option:int):
    '''
    #入力された文章を,SudachiDictとUserDictで翻訳
    '''
    #ユーザー辞書のパスを宣言
    config_path_link = "../lib/python3.9/site-packages/sudachipy/resources/sudachi.json"
    #ユーザー辞書の使用を宣言
    tokenizer_obj = d.Dictionary(config_path=config_path_link).create() 
    mode = t.Tokenizer.SplitMode.C
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