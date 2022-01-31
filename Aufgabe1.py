import pandas as pd
import math
from matplotlib import pyplot as plt
from LoadData import pullMasie
import numpy as np
#pullMasie()

df = pd.read_csv('masie_4km_allyears_extent_sqkm.csv', header=1, delimiter=',')

def getName(name):
    liste=['0','1','2','3','4','5','6','7','8','9']
    while (name[0] == ' ' or name[0] == '(' or name[0] == ')'or name[0] in liste):
        name = name[1:]
    return name

def mvgAvg(liste, window=30):
    avg = []
    start = math.floor(window / 2)
    end = len(liste) - start
    for i in range(end):
        if i >= start:
            value = 0
            for j in range(i - start, i + start + 1):
                value = value + liste[j]
            value = value / window
            avg.append(value)
    return avg



def columnPicker(df):
    counter = 0
    for column in df:
        if (counter >= 1 and counter<len(df.columns)):
            actColumn = df[column]
            avg = mvgAvg(actColumn)
            name=getName(column)
            plt.title(name)
            plt.xlabel('Jahr')
            plt.ylabel('SQKM')
            plt.xticks(np.arange(0, len(actColumn), 363.0),
                       ['06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17','18','19','20','21','22'])
            plt.plot(actColumn, color='blue')
            plt.plot(avg, color='red')
            plt.show()
        elif (counter >= 18):
            break;
        counter = counter + 1

def start():
    columnPicker(df)

start()
