import pandas as pd
import math
from matplotlib import pyplot as plt

df = pd.read_csv('masie_1km_allyears_extent_sqkm.csv', header=1, delimiter=',')
x = df['yyyyddd']


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


def useColumns():
    counter = 0
    for i in df:
        if (counter>=1 and counter < 18):
            column = df[i]
            avg = mvgAvg(column)
            plt.plot(column, color='blue')
            plt.plot(avg, color='red')
            plt.show()
        elif(counter>=18):
            break;
        counter = counter + 1

useColumns()
