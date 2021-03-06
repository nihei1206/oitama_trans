from sudachipy import tokenizer as t
from sudachipy import dictionary as d
# from nltk.util import ngrams
from nltk import bleu_score as bs
from translator import translate

def hyokaArray_trans(text:str) -> list:
    """
    #入力された文章を,評価するための配列にsudachidictのみでわかち書き
    #splitMode == A
    """
    ### Initialized Takenizer ### 
    mode = t.Tokenizer.SplitMode.A
    config_path_link = "../lib/python3.9/site-packages/sudachipy/resources/notuse_resources/sudachi.json"
    tokenizer_obj = d.Dictionary(config_path=config_path_link,dict="full").create()
    hyokaArray = []
    tokens = tokenizer_obj.tokenize(text,mode)
    for m in tokens:
        hyokaArray.append(m.surface()+str(m.part_of_speech()))
    return hyokaArray
    # surface()+part_of_speech() -> (表層形 + 品詞情報[例:動詞/五段活用/さ変可能]) 


def bleu_score(resultHyokaArray,answerHyokaArray):
    bleuScore = bs.sentence_bleu([resultHyokaArray],answerHyokaArray,smoothing_function=bs.SmoothingFunction().method7)
    if bleuScore == 0:
        return None
    else:
        bleuScore = float(bleuScore)
        return bleuScore

def list_difference(list1:list, list2:list) -> list:
    """
    #配列差分出力関数
    #list1にあって、list2にない要素を出力
    #list1に重複{2つ同じ要素}があったら、2つとカウント。
    #list2に同一要素が1つだとしたら、1つだけ出力される
    """
    result = list1.copy()
    for value in list2:
        if value in result:
            result.remove(value)
    return result

def translate_hyoka(oitama:str, answer:str ,option:int) -> list:
    """
    hyokaOption == 0 ->置換のみ手法
    hyokaOption == 1 -> 脳筋Option(格助詞の確立的はめ込み)
    #return [answer:str,oitama:str,result:str,fScore:float,bleuScore:float]
    """
    #置賜弁をここで標準語に翻訳
    result = translate.replacement(oitama,option)

    #result:置賜弁を翻訳した結果
    #answer:用意している正解データ
    resultHyokaArray = hyokaArray_trans(result)
    answerHyokaArray = hyokaArray_trans(answer)

    # 正解データをわかち書き
    # 正解文を形態要素解析した正解配列と翻訳したあとの文を形態要素解析した配列を比較して、
    # 正解分にしかない配列の要素を配列にして出力したのがOnly_answer_list_have
    Only_answer_list_have = list_difference(answerHyokaArray,resultHyokaArray)
    system_output_word_count = len(resultHyokaArray) #翻訳した結果の全単語数
    answer_output_word_count = len(answerHyokaArray) #対応する正解データの全単語数
    correct_output_word_count = answer_output_word_count-len(Only_answer_list_have)

    seido = 0
    saigen = 0

    try:
        seido = correct_output_word_count/system_output_word_count
        saigen = correct_output_word_count/answer_output_word_count
    except ZeroDivisionError as e:
        print(e)
        print(type(e))

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
    bleuScore = bleu_score(resultHyokaArray,answerHyokaArray)

    # input = (oitama:str , answer:str)

    return [oitama,result,answer,fScore,bleuScore]
