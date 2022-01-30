# import sudachipy
from sudachipy import tokenizer
from sudachipy import dictionary


# トークナイザの作成,辞書位置(sudachi.json ; 相対パス)の指定
# Qsudachidict_full優先 dict="full"
# mode(a,b,c)の指定
config_path_link = "lib/python3.9/site-packages/sudachipy/resources/sudachi.json"
tokenizer_obj = dictionary.Dictionary(config_path=config_path_link).create() 
mode = tokenizer.Tokenizer.SplitMode.C

# 置賜弁辞書とシステム辞書を元にわかち書きを行い、置賜弁->標準語へ置き換え後接続する関数
# output type(list)
# [0]->それぞれのわかち書きに対して、方言or Not表記
# [1]->標準語変換,結合後の文章
def transOitamaToJp(text,mode,tokenizer_obj):
    combinedExchangeHogen = []
    hogenOrNotArray = []
    tokens = tokenizer_obj.tokenize(text,mode)
    for m in tokens:
        if m.part_of_speech()[5] == '方言':
            hogenOrNotArray.append(m.surface()+':方言->'+m.normalized_form()+':標準語')
            combinedExchangeHogen.append(m.normalized_form())
        else:
            hogenOrNotArray.append(m.surface()+':標準語')
            combinedExchangeHogen.append(m.surface())
    return combinedExchangeHogen,hogenOrNotArray

text = input()
print(transOitamaToJp(text,mode,tokenizer_obj)[0])
print(transOitamaToJp(text,mode,tokenizer_obj)[1])

# list -> str
text = "".join(transOitamaToJp(text,mode,tokenizer_obj)[0])

tokenizer_obj = dictionary.Dictionary(dict="full").create() #Qsudachidict_full優先 dict="full"
mode = tokenizer.Tokenizer.SplitMode.C

# 標準語を入力し単純にわかち書きして配列で出力する関数
def wakachiWrite(text,mode,tokenizer_obj):
    tokens = tokenizer_obj.tokenize(text,mode)
    wakachi_Array = []
    for m in tokens:
        wakachi_Array.append(m.surface())
    return wakachi_Array

# output type;list
print(wakachiWrite(text,mode,tokenizer_obj))
# list -> strs
print("".join(wakachiWrite(text,mode,tokenizer_obj)))

#### Sudachipy Memo ####
#m.surface() # => '食べ'
#m.dictionary_form() # => '食べる'
#m.reading_form() # => 'タベ'
#m.part_of_speech() # => ['動詞', '一般', '*', '*', '下一段-バ行', '連用形-一般']
#m.normalized_form() => 正規化

#https://github.com/WorksApplications/SudachiPy/blob/develop/docs/tutorial.md
#https://evrythingonmac.blogspot.com/2019/12/sudachipy-sudachidictfull-update.html
#https://ohke.hateblo.jp/entry/2019/03/09/101500