# import sudachipy
from sudachipy import tokenizer
from sudachipy import dictionary
import collections
import copy

config_path_link = "lib/python3.9/site-packages/sudachipy/resources/sudachi.json"
tokenizer_obj = dictionary.Dictionary(config_path=config_path_link).create() 
mode = tokenizer.Tokenizer.SplitMode.A

result = 'これから服を脱いでね,これからあああ'
answer = 'これから服を脱いでね,これから,,'

def transOitamaToJp(text,mode,tokenizer_obj):
    combinedExchangeHogen = []
    tokens = tokenizer_obj.tokenize(text,mode)
    for m in tokens:
        if m.part_of_speech()[5] == '方言':
            combinedExchangeHogen.append([m.normalized_form()+str(m.part_of_speech())])
        else:
            combinedExchangeHogen.append([m.surface()+str(m.part_of_speech())])
    return combinedExchangeHogen


def list_difference(list1, list2):
    result = list1.copy()
    for value in list2:
        if value in result:
            result.remove(value)
    return result

Only_result_list_have = list_difference(transOitamaToJp(result,mode,tokenizer_obj),transOitamaToJp(answer,mode,tokenizer_obj))
print(Only_result_list_have,"Only_result_list_have:"+str(len(Only_result_list_have)))

Only_answer_list_have = list_difference(transOitamaToJp(answer,mode,tokenizer_obj),transOitamaToJp(result,mode,tokenizer_obj))
print(Only_answer_list_have,"Only_answer_list_have:"+str(len(Only_answer_list_have)))


print("system output words:" + str(len(transOitamaToJp(result,mode,tokenizer_obj))))
#print("correct output of system:" + str(len()))

system_output_word_count = len(transOitamaToJp(result,mode,tokenizer_obj))
answer_output_word_count = len(transOitamaToJp(answer,mode,tokenizer_obj))
correct_output_word_count = answer_output_word_count-len(Only_answer_list_have)
seido = correct_output_word_count/system_output_word_count
saigen = correct_output_word_count/answer_output_word_count

print("精度:" + str(seido))
print("再現率:" + str(saigen))
print("F値" + str((2*seido*saigen)/(seido+saigen)))