from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

# read csv-data in dataframe
df = pd.read_csv('masie_4km_allyears_extent_sqkm.csv', header=1, delimiter=',')


# get column name that represents specific region
def getName(name):
    liste = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    while (name[0] == ' ' or name[0] == '(' or name[0] == ')' or name[0] in liste):
        name = name[1:]
    return name


# calculate specific percentil
def calcPerzent(liste, perzentil):
    liste = pd.DataFrame(liste)
    wert = liste.quantile(q=perzentil / 100)
    return wert


# calculate minimum of list
def calcMin(liste):
    liste = pd.DataFrame(liste)
    wert = liste.min()
    return wert


# calculate maximum of list
def calcMax(liste):
    liste = pd.DataFrame(liste)
    wert = liste.max()
    return wert


# arrange values in lists to perform min, max, quantiles
def minMax(column, dateList, columnCounter):
    minList = []
    maxList = []

    perzent25 = []
    perzent50 = []
    perzent75 = []

    # arrange numbers to required format to compare them
    for j in range(1, 365):
        liste_tageswerte = []
        if (j < 10):
            date = '00' + str(j)
        elif (j < 100):
            date = '0' + str(j)
        else:
            date = str(j)
        # iterate over values in actual column
        for z in range(0, len(column)):
            dateCompare = str(dateList[z])
            # convert date value in specific format to compare actual year
            dateEquation = dateCompare[4:]
            # compare actual date value with entries in date-list
            if (date in dateEquation):
                liste_tageswerte.append(column[z])

        # calculate min/max and append value to related list
        minList.append(calcMin(liste_tageswerte))
        maxList.append(calcMax(liste_tageswerte))

        # calculate 25, 50, 75 % percentile and append to related list
        perzent25.append(calcPerzent(liste_tageswerte, 25))
        perzent50.append(calcPerzent(liste_tageswerte, 50))
        perzent75.append(calcPerzent(liste_tageswerte, 75))

    # build plot
    plt.xlabel('Monat')
    plt.ylabel('Ice Extent in [sqkm]')
    plt.title('Min Max Plot Region: ' + str(columnCounter))
    plt.xticks(np.arange(0, 365, 30.5),
               ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'])
    # add min/max and percentile lists to plot
    plt.plot(maxList, color='blue', label='Maximum')
    plt.plot(perzent75, color='cyan', label='Perzentil 75')
    plt.plot(perzent50, color='yellow', label='Perzentil 50')
    plt.plot(perzent25, color='red', label='Perzentil 25')
    plt.plot(minList, color='green', label='Minimum')
    counter = 0
    for i in minList:
        counter = counter + 1
    plt.legend()
    plt.show()


# function for plotting seasonal plot
def plotSeasonal(column, dateList, columnCounter):
    # define color gradient
    colorBlue = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    colorRed = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    colorAlpha = [1, 0.875, 0.75, 0.625, 0.5, 0.375, 0.25, 0.125, 0.05, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]

    colorCounter = 0

    # arrange numbers to required format to compare them
    for j in range(2006, 2022):
        seasonal_plot = []
        colorCounter = colorCounter + 1

        # iterate over values in actual column
        for z in range(0, len(column)):
            dateCompare = str(dateList[z])
            # convert date value in specific format to compare actual year
            yearEquation = dateCompare[:4]

            # compare date value as string with entries in year-list
            if (str(j) in yearEquation):
                seasonal_plot.append(column[z])

        # build plot
        plt.title('Seasonal Plot Region: ' + str(columnCounter))
        plt.xlabel('Monat')
        plt.ylabel('Ice Extent in [sqkm]')
        plt.xticks(np.arange(0, 365, 31.0),
                   ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'])
        plt.plot(seasonal_plot, label=str(j),
                 color=(colorRed[colorCounter], 0, colorBlue[colorCounter], colorAlpha[colorCounter]))
        ##ging nicht mit cmap = seismic

    # show legend on right side of figure
    plt.legend(bbox_to_anchor=(1.15, 1.0))
    plt.show()


# start function: calls other functions and runs whole program
def start(df):
    dateList = df['yyyyddd']
    # iterate over all columns; except date-column
    for column in df:
        if column != 'yyyyddd':
            name = getName(column)
            print('Durchgang: ' + str(name))
            actColumn = df[column]
            minMax(actColumn, dateList, name)
            plotSeasonal(actColumn, dateList, name)


# call start-function
start(df)
