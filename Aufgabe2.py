##eigentlich darf nichts an den Werten geändert werden
##da 0 ja einfach nur beduetet, das kein Eis vorhanden ist





import pandas as pd
import math
from matplotlib import pyplot as plt

df = pd.read_csv('masie_1km_repaired.csv', header=1, delimiter=',')
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
        if (counter >= 1 and counter < 18):
            column = df[i]
            avg = mvgAvg(column)
            plt.plot(column, color='blue')
            plt.plot(avg, color='red')
            plt.show()
        elif (counter >= 18):
            break;
        counter = counter + 1


# useColumns()



dfRepaired = df
"""
import missingno as msno
msno.matrix(dfRepaired)
plt.show()
"""

from sklearn.impute import SimpleImputer


#füllt die fehldenen Werte mit dem Durchschnitt auf
def repairColumns():
    counter = 0
    for i in dfRepaired:
        if (counter >= 1 and counter < 18):
            imp_mean=SimpleImputer(missing_values=0.00,strategy='mean')
            dfRepaired[i]=imp_mean.fit_transform(dfRepaired[i].values.reshape(-1,1))
            dfRepaired[i]=dfRepaired[i].astype(int)
        elif (counter >= 18):
            break
        counter = counter + 1


repairColumns()

# Dropper Function
"""
# kürzt x Werte auf den Avg
def dropper(liste, window=30):
    x2 = liste
    i = 0
    while i < window / 2:
        # löscht erstes und letztes Item
        x2.pop(0)
        x2.pop()
        i = i + 1
    return x2
"""
