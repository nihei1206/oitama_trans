import csv
import datetime
import numpy as np
import matplotlib.pyplot as plt
import statistics as st


def makeFig(array, data_name:str,bins:int,sub_name,title:str,dataType):
    median = st.median(array)
    ave = st.mean(array)
    plt.style.use('ggplot')
    plt.figure(figsize=(10, 10), dpi=40)
    plt.hist(array,bins=bins,range = (0,1), color="blue", edgecolor="black", linestyle="--",rwidth = 0.8)
    plt.title(title, fontsize = 24,color = 'k') 
    plt.xticks(fontsize = 32,color = 'k', fontweight = 'bold')
    plt.xlabel("F-score", fontsize=24,color = 'k') 
    plt.ylabel("Frequency", fontsize=24,color = 'k')

    if dataType == 's':
        plt.yticks(np.arange(0, 65, 5),fontsize=32, fontweight = 'bold',color = 'k')
    if dataType == 't':
        plt.yticks(np.arange(0, 22, 2),fontsize=32, fontweight = 'bold',color = 'k')

    dt_now = datetime.datetime.now()
    plt.savefig("../outputFig/" +str(data_name) + str(sub_name)+ dt_now.strftime('%H%M%S'))
    plt.show()
    
    return "Done! " + str(data_name) + str(sub_name)+ ": median is " + str(median) +  " / Ave is " + str(ave)

def selectFigType():
    """
    図を作りたい
    """

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
    print('input import file name')
    imported_csvname = str(input())


    with open("../outputCSV/" + imported_csvname) as f:
        reader = csv.reader(f)
        inputArray = [row for row in reader]
    f.close()

    inputArray = np.array(inputArray[1:-1])

    if dataType == 'split' or  dataType == 's':
        floatArray = np.array(inputArray.transpose(1, 0)[4],dtype = np.float64)
        print(makeFig(floatArray,dataname,bins,title,dataType))
    elif dataType == 'trans' or  dataType == 't':
        floatArray = np.array(inputArray.transpose(1, 0)[3],dtype = np.float64)
        print(makeFig(floatArray,dataname,bins,title,dataType))

        floatArray = np.array(inputArray.transpose(1, 0)[6],dtype = np.float64)
        print(makeFig(floatArray,dataname,bins,title,dataType))

