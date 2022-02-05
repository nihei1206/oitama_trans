from chikkarpy import Chikkar
from chikkarpy.dictionarylib import Dictionary
from sudachipy import tokenizer
from sudachipy import dictionary
import numpy as np
import unicodedata

    # config_path_link = "lib/python3.9/site-packages/sudachipy/resources/sudachi.json"
    # tokenizer_obj = dictionary.Dictionary(config_path=config_path_link).create() 
    # mode = tokenizer.Tokenizer.SplitMode.C

def noukinTrans(text:str) -> str :
    list_str = list(text)
    outputArray =[]
    for i in range(len(list_str)):
        hiragana = unicodedata.normalize("NFKD",list_str[i])[0]
        outputArray.append(hiragana)
        outputStr = "".join(outputArray)
    return outputStr

print(noukinTrans("いぎだぐ"))

