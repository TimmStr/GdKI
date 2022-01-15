##eigentlich darf nichts an den Werten geändert werden
##da 0 ja einfach nur beduetet, das kein Eis vorhanden ist


import pandas as pd
import math
from matplotlib import pyplot as plt
import csv
df = pd.read_csv('masie_4km_repaired.csv', header=1, delimiter=',')
x = df['yyyyddd']



def csvInserter(counter,row):
    with open('masie_4km_repaired.csv','r')as readFile:
        reader=csv.reader(readFile)
        lines=list(reader)
        lines.insert(counter,row)
    with open('masie_4km_repaired.csv','w')as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    readFile.close()
    writeFile.close()







def insertNumbers(dateList,df):
    compareList=[]
    test=False
    counter=1
    for y in range(2006, 2021):
        for d in range(1, 366):
            if (d < 10):
                date = '00' + str(d)
            elif (d < 100):
                date = '0' + str(d)
            else:
                date = str(d)
            date=' '+str(y)+str(date)
            compareList.append(date)
            counter=counter+1

        for i in range(0, len(dateList)):

            dateCompare = str(dateList[counter])

            if(dateCompare not in compareList):
                print(date)
                print(dateCompare)
                row = []
                for column in df:
                    if(column=='yyyyddd'):
                        row.append(date)
                    else:
                        mean_df=df[column].mean()
                        gerundet=round(mean_df,2)
                        row.append(str(gerundet))
                csvInserter(counter,row)
            else:
                # print('enthalten')
                print()
            break
        break


def columnPicker(df):
    counter = 0
    for column in df:
        if (counter >= 1 and counter<len(df.columns)):
            insertNumbers(x,df)
        elif (counter >= 18):
            break
        counter = counter + 1

def start():
    columnPicker(df)

start()