# このファイルは、mainとしてどの関数を実行するかCLI上で選べる程度の機能のみつける
import make_figure as mf ,make_csv as mc

def choice(number):
    if number == 0:
        # split_hyoka()
        print('start hyoka def')
        i = int(input())
        print(i)
        mc.make_csv_split()

    elif number == 1:
        # translate_hyoka()
        print('start translate def')
        print('what option you use')
        print('0:Base','1:格助詞補完')
        option = int(input())
        if not (option == 0 or option == 1):
            exit()
        print('何回ぶん回しますか?')
        n = int(input())
        mc.make_csv_translate(n,option)

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
        print('title of histgram')
        title = str(input())

        mf.selectFigType(dataname,dataType,bins,title)
    else:
        exit()

if __name__ == '__main__':
    print("なにをしますか?")
    print('0:分割と評価','1:翻訳と評価','2:作図')
    selectFanction = int(input())
    choice(selectFanction)


    