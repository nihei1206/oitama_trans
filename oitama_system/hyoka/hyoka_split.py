from sudachipy import tokenizer as t
from sudachipy import dictionary as d

def sudachionlyWakachi(text:str) -> list:
    """
    sudachi_dictだけでの分割
    """
    hyokaArrayonly = []
    mode = t.Tokenizer.SplitMode.A
    config_path_link = "../lib/python3.9/site-packages/sudachipy/resources/notuse_resources/sudachi.json"
    tokenizer_obj = d.Dictionary(config_path=config_path_link,dict="full").create()
    tokens = tokenizer_obj.tokenize(text,mode)
    for m in tokens:
        hyokaArrayonly.append(m.surface())
    return hyokaArrayonly

def sudachiOitamaWakachi(text:str) -> list:
    """
    sudachi_dictとOitama_dictでの分割
    """
    outputArray = []
    mode = t.Tokenizer.SplitMode.A
    config_path_link = "../lib/python3.9/site-packages/sudachipy/resources/sudachi.json"
    tokenizer_obj = d.Dictionary(config_path=config_path_link,dict="full").create()
    tokens = tokenizer_obj.tokenize(text,mode)
    for m in tokens:
        outputArray.append(m.surface())
    return outputArray

def hyoka(result:list,answer:list) -> list:
    """
    fig.8-1:
    return result,answer,precision,recall,Fscore
    """
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
    """
    ,分割
    """
    outputArray = text.split(',')
    return outputArray


