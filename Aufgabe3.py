from matplotlib import pyplot as plt
import pandas as pd

df = pd.read_csv('masie_4km_allyears_extent_sqkm.csv', header=1, delimiter=',')


def minMax(column, dateList, columnCounter):
    minList = []
    maxList = []

    # bringen der Zahlen ins richtige Zahlenformat damit Vergleich ermöglicht wird
    for j in range(1, 365):
        min = column[j - 1]
        max = column[j - 1]
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
            yearEquation = dateCompare[:4]

            # Abfrage ob bearbeiteter Wert aus For Schleife in Einträgen der Spalte Datum ist
            if (date in dateEquation):
                if min > column[z]:
                    min = column[z]
                if max < column[z]:
                    max = column[z]
        minList.append(min)
        maxList.append(max)
    plt.xlabel('Tage')
    plt.ylabel('SQKM')
    plt.title('Min Max Function   Column: ' + str(columnCounter))
    plt.plot(maxList, color='blue', label='Maximum')
    plt.plot(minList, color='green', label='Minimum')
    plt.legend()
    plt.show()


def plotSeasonal(column, dateList, columnCounter):
    colorBlue = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    colorRed = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    colorAlpha = [1, 0.875, 0.75, 0.625, 0.5, 0.375, 0.25, 0.125, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]
    # columnCounter = 0
    # For Schleife für Spalten aus DF

    colorCounter = 0

    # bringen der Zahlen ins richtige Zahlenformat damit Vergleich ermöglicht wird
    for j in range(2006, 2021):
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
        plt.xlabel('Tage')
        plt.ylabel('SQKM')
        plt.plot(secondPlot, label=str(j),
                 color=(colorBlue[colorCounter], 0, colorRed[colorCounter], colorAlpha[colorCounter]))

    plt.legend()
    plt.show()


def start(df):
    columnCounter = 0
    dateList = df['yyyyddd']
    for column in df:
        minList = []
        maxList = []
        if (columnCounter >= 1 and len(df.columns)):
            print('Durchgang' + str(columnCounter))
            actColumn = df[column]
            colorCounter = 0
            minMax(actColumn, dateList, columnCounter)
            plotSeasonal(actColumn, dateList, columnCounter)
        elif (columnCounter >= 18):
            print(minList)
            print(maxList)
            break;
        columnCounter = columnCounter + 1


start(df)
