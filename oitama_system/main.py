# このファイルは、mainとしてどの関数を実行するかCLI上で選べる程度の機能のみつける
import make_figure as mf ,make_csv as mc

def choice(number):
    if number == 0:
        # split_hyoka()
        mc.make_csv_split()

    elif number == 1:
        # translate_hyoka()
        mc.make_csv_translate()

    elif number == 2:
        # makefig()
        mf.selectFigType()
    else:
        exit()

if __name__ == '__main__':
    print("なにをしますか?")
    print('0:分割と評価','1:翻訳と評価','2:作図')
    selectFanction = int(input())
    choice(selectFanction)