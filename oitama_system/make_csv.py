import time
import csv
import datetime
from tqdm import tqdm
import numpy as np
from statistics import mean
from translator import translate as tr,option as op
from hyoka import hyoka_trans as ht,hyoka_split as hs

def average_output(array:list,option:int) -> list:
    # option 0 => for split evaluate CSV
    if option == 0:
        seido_arr = []
        saigen_arr = []
        fscore_arr = []
        for i in range(len(array)):
            seido_arr.append(array[i][2])
            saigen_arr.append(array[i][3])
            fscore_arr.append(array[i][4])
        seido_ave = mean(seido_arr)
        saigen_ave = mean(saigen_arr)
        f_ave = mean(fscore_arr)
        return '平均',None,seido_ave,saigen_ave,f_ave
    
    if option == 1:
        # option 1 => for translate evaluate CSV
        numarr = np.array(array).transpose()
        f_ave = mean(numarr[3])
        f_op_ave = mean(numarr[6])
        index_ave = mean(numarr[7])
        # bleu_ave = mean(numarr[4])
        return '平均',None,None,f_ave,None,None,f_op_ave,index_ave


def make_csv_split():
    '''

    '''

    start = time.time()
    with open('../auto_evaluation.csv') as f:
        reader = csv.reader(f)
        inputArray = [row for row in reader]
    f.close()

    outputArray = []
    for i in tqdm(range(1,len(inputArray))):
        np.pi*np.pi
        outputArray.append(hs.hyoka(hs.sudachiOitamaWakachi(inputArray[i][1]),hs.canmaBunkatsu(inputArray[i][2])))
    
    outputArray.append(average_output(outputArray,0))

    header = ['result','answer','seido','saigen','Fscore']
    dt_now = datetime.datetime.now()
    with open('../outputCSV/Bunkatsu_OitamaDict'+ dt_now.strftime('%y%m%d-%H%M%S') +'.csv', 'w') as f:

        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(outputArray)

    f.close()
        
    outputArray = []
    for i in tqdm(range(1,len(inputArray))):
        np.pi*np.pi
        outputArray.append(hs.hyoka(hs.sudachionlyWakachi(inputArray[i][1]),hs.canmaBunkatsu(inputArray[i][2])))

    outputArray.append(average_output(outputArray,0))
    header = ['result','answer','seido','saigen','Fscore']
    dt_now = datetime.datetime.now()
    with open('../outputCSV/Bunkatsu_sudachiDict'+ dt_now.strftime('%y%m%d-%H%M%S') +'.csv', 'w') as f:

        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(outputArray)

    f.close()
    elapsed_time = time.time() - start

    return print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

def make_csv_translate(n_time:int):
    '''
    
    '''

    start = time.time()
    with open('../auto_evaluation.csv') as f:
        reader = csv.reader(f)
        inputArray = [row for row in reader]
    f.close()

    outputArray = []
    for i in tqdm(range(1,len(inputArray))):
        np.pi*np.pi
        adMF = ht.translate_hyoka(inputArray[i][1],inputArray[i][0],0)
        adMF.append(tr.replacement(inputArray[i][1],1))
        # ぶん回す↓
        manytime = op.manytimeFscore(inputArray[i][1],inputArray[i][0],n_time)
        adMF.append(manytime[0])
        adMF.append(manytime[1])
        outputArray.append(adMF)
        # np.pi*np.pi
        # adMF = translate_hyoka(inputArray[i][1],inputArray[i][0],0)
        # adMF.append(translaterOitamaOption(inputArray[i][1],tokenizer_obj))


    outputArray.append(average_output(outputArray,1))

    # for_plot_array
    header = ['oitama','result','answer','fScore','bleuscore','option_result','opt_Arr_max','maxtimesIndex']
    dt_now = datetime.datetime.now()
    with open('../outputCSV/OitamaTrans'+ dt_now.strftime('%y%m%d-%H%M%S') +'.csv', 'w') as f:

        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(outputArray)

    f.close()
    elapsed_time = time.time() - start
    return print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    


