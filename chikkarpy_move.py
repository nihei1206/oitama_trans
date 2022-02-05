from chikkarpy import Chikkar
from chikkarpy.dictionarylib import Dictionary
from sudachipy import tokenizer
from sudachipy import dictionary

chikkar = Chikkar()

# デフォルトのシステム同義語辞書を使う場合，Dictionaryの引数は省略可能 You may omit the ``Dictionary`` arguments if you want to use the system synonym dictionary
system_dic = Dictionary()
chikkar.add_dictionary(system_dic)

print(chikkar.find("閉店"))
# => ['クローズ', 'close', '店仕舞い']

print(chikkar.find("閉店", group_ids=[5])) # グループIDによる検索 Search by group ID
# => ['クローズ', 'close', '店仕舞い']

print(chikkar.find("開放"))
# => ['オープン', 'open']

chikkar.enable_verb() # 用言の出力制御（デフォルトは体言のみ出力） Output control of verbs (default is to output only nouns)
print(chikkar.find("開放"))
# => ['開け放す', '開く', 'オープン', 'open']

config_path_link = "lib/python3.9/site-packages/sudachipy/resources/sudachi.json"
#ユーザー辞書の使用を宣言
mode = tokenizer.Tokenizer.SplitMode.C
tokenizer_obj = dictionary.Dictionary().create()
morphs = tokenizer_obj.tokenize('おしょうしな')
print(morphs[0].begin()),print('begin')
print(morphs[0].end()),print('end')
print(morphs[0].surface()),print('surface')
print(morphs[0].part_of_speech()),print('part_of_speech')
print(morphs[0].part_of_speech_id()),print('part_of_speech_id')
print(morphs[0].dictionary_form()),print('dictionary_form')
print(morphs[0].normalized_form()),print('normalized_form')
print(morphs[0].reading_form()),print('reading_form')
print(morphs[0].is_oov()),print('is_oov')
print(morphs[0].word_id()),print('word_id')
print(morphs[0].dictionary_form()),print('dictionary_form')
print(morphs[0].dictionary_id()),print('dictionary_id')
print(morphs[0].synonym_group_ids()),print('synonym_group_ids')
morphs = tokenizer_obj.tokenize("OutOfVocab")
print(morphs[0].is_oov())