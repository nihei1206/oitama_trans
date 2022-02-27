# このファイルは、mainとしてどの関数を実行するかCLI上で選べる程度の機能のみつける
import makefigure
from hyoka import hyoka_trans,hyoka_split

def choice(number):
    if number == 0:
        # hyoka()
        print('start hyoka def')
        i = int(input())
        print(i)
        hyoka_split.importArrayfromCSV_then_do()

    elif number == 1:
        # translate()
        print('start translate def')
        print('what option you use')
        print('0:Base','1:格助詞補完')
        option = int(input())
        if not (option == 0 or option == 1):
            exit()
        print(option)

        print('何回ぶん回しますか?')
        n = int(input())
        hyoka_trans.importArrayfromCSV_then_do(n)

    elif number == 2:
        # makefig()
        print('start makefig def')
        print('split(s) or trans(t)')
        dataType = str(input())
        if dataType == 'split' or dataType == 's':
            print('Oitama or Sudachi')
            dataname = str(input())
        elif dataType == 'trans' or dataType == 't':
            dataname = str('Translator')
        print('input bins')
        bins = int(input())
        makefigure.selectFigType(dataname,dataType,bins)
    else:
        exit()

if __name__ == '__main__':
    print("なにをしますか?")
    print('0:分割と評価','1:翻訳と評価','2:作図')
    selectFanction = int(input())
    choice(selectFanction)


    