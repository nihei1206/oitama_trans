# このファイルは、mainとしてどの関数を実行するかCLI上で選べる程度の機能のみつける
import make_figure as mf ,make_csv as mc

def choice(number):
    if number == 0:
        # split_hyoka()
        mc.make_csv_split()

    elif number == 1:
        # translate_hyoka()
        print('何回ぶん回しますか?')
        n = int(input())
        mc.make_csv_translate(n)

    elif number == 2:
        # makefig()
        print('split(s) or trans(t)')
        dataType = str(input())
        if dataType == 's':
            print('Oitama or Sudachi')
            dataname = str(input())
        elif dataType == 't':
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


    