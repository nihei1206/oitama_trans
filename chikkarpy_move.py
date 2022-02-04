from chikkarpy import Chikkar
from chikkarpy.dictionarylib import Dictionary

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