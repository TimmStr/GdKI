from matplotlib import pyplot as plt
import pandas as pd
from LoadData import pullMasie
import numpy as np

#pullMasie()
df = pd.read_csv('masie_4km_allyears_extent_sqkm.csv', header=1, delimiter=',')

def getName(name):
    liste = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    while (name[0] == ' ' or name[0] == '(' or name[0] == ')' or name[0] in liste):
        name = name[1:]
    return name

def calcPerzent(liste, perzentil):
    liste=pd.DataFrame(liste)
    wert=liste.quantile(q=perzentil/100)
    return wert

def calcMin(liste):
    liste=pd.DataFrame(liste)
    wert=liste.min()
    return wert

def calcMax(liste):
    liste=pd.DataFrame(liste)
    wert=liste.max()
    return wert

def minMax(column, dateList, columnCounter):
    minList = []
    maxList = []

    perzent25 = []
    perzent50 = []
    perzent75 = []

    # bringen der Zahlen ins richtige Zahlenformat damit Vergleich ermöglicht wird
    for j in range(1, 365):
        liste_tageswerte = []
        if (j < 10):
            date = '00' + str(j)
        elif (j < 100):
            date = '0' + str(j)
        else:
            date = str(j)
        # fürs ablaufen aller Einträge in actColumn
        for z in range(0, len(column)):
            dateCompare = str(dateList[z])
            # umformatieren in Format zum Vergleich. Bei nr 019 kam auch 2019 anstatt Tag 019
            dateEquation = dateCompare[4:]
            # Abfrage ob bearbeiteter Wert aus For Schleife in Einträgen der Spalte Datum ist
            if (date in dateEquation):
                liste_tageswerte.append(column[z])

        minList.append(calcMin(liste_tageswerte))
        maxList.append(calcMax(liste_tageswerte))
        # Perzent hat alle Objekte zur aktuellen Spalte mit dem Datum xy
        # Aufruf Methode zum Perzentil berechnen
        perzent25.append(calcPerzent(liste_tageswerte, 25))
        perzent50.append(calcPerzent(liste_tageswerte, 50))
        perzent75.append(calcPerzent(liste_tageswerte, 75))

    plt.xlabel('Monat')
    plt.ylabel('SQKM')
    plt.title('Min Max Function   Column: ' + str(columnCounter))
    plt.xticks(np.arange(0, 365, 30.5))
               #,
               #['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'])
    plt.plot(maxList, color='blue', label='Maximum')
    plt.plot(perzent75, color='cyan', label='Perzentil 75')
    plt.plot(perzent50, color='yellow', label='Perzentil 50')
    plt.plot(perzent25, color='red', label='Perzentil 25')
    plt.plot(minList, color='green', label='Minimum')
    counter=0
    for i in minList:
        counter=counter+1
        print(counter)
        print(i)
    plt.legend()
    plt.show()


def plotSeasonal(column, dateList, columnCounter):
    colorBlue = [1, 1, 1, 1, 1, 1, 1, 1, 0,0, 0, 0, 0, 0, 0, 0, 0]
    colorRed = [0, 0, 0, 0, 0, 0, 0, 0, 1,1, 1, 1, 1, 1, 1, 1, 1]
    colorAlpha = [1, 0.875, 0.75, 0.625, 0.5, 0.375, 0.25, 0.125, 0.05,0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]
    # For Schleife für Spalten aus DF

    colorCounter = 0

    # bringen der Zahlen ins richtige Zahlenformat damit Vergleich ermöglicht wird
    for j in range(2006, 2022):
        secondPlot = []
        colorCounter = colorCounter + 1

        # fürs ablaufen aller Einträge in actColumn
        for z in range(0, len(column)):
            dateCompare = str(dateList[z])
            # umformatieren in Format zum Vergleich. Jahr
            yearEquation = dateCompare[:4]

            # Abfrage ob bearbeiteter Wert aus For Schleife in Einträgen der Spalte Datum ist
            if (str(j) in yearEquation):
                secondPlot.append(column[z])

        plt.title('Seasonal Function   Column: ' + str(columnCounter))
        plt.xlabel('Monat')
        plt.ylabel('SQKM')
        plt.xticks(np.arange(0, 365, 31.0),['Jan','Feb','Mär','Apr','Mai','Jun','Jul','Aug','Sep','Okt','Nov','Dez'])
        plt.plot(secondPlot, label=str(j),
                 color=(colorBlue[colorCounter], 0, colorRed[colorCounter], colorAlpha[colorCounter]))
        ##ging nicht mit cmap = seismic

    plt.legend()
    plt.show()


def start(df):
    columnCounter = 0
    dateList = df['yyyyddd']
    for column in df:
        if (columnCounter >= 1 and columnCounter < len(df.columns)):
            name = getName(column)
            print('Durchgang' + str(columnCounter))
            actColumn = df[column]
            minMax(actColumn, dateList, name)
            plotSeasonal(actColumn, dateList, name)
        elif (columnCounter >= 18):
            break;
        columnCounter = columnCounter + 1


start(df)