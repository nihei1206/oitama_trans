from sudachipy import tokenizer
from sudachipy import dictionary
from nltk.util import ngrams
from nltk import bleu_score
from statistics import mean
from translator import translate

def hyokaArray_trans(text:str,tokenizer_obj:tokenizer.Tokenizer) -> list:
    '''
    #入力された文章を,評価するための配列にsudachidictのみでわかち書き
    #splitMode == A
    '''
    ### Initialized Takenizer ### 
    mode = tokenizer.Tokenizer.SplitMode.A
    config_path_link = "lib/python3.9/site-packages/sudachipy/resources/notuse_resources/sudachi.json"
    tokenizer_obj = dictionary.Dictionary(config_path=config_path_link,dict="full").create()
    hyokaArray = []
    tokens = tokenizer_obj.tokenize(text,mode)
    for m in tokens:
        hyokaArray.append(m.surface()+str(m.part_of_speech()))
    return hyokaArray

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
    
    result = translate.replacement(oitama,tokenizer_obj,hyokaOption)

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

