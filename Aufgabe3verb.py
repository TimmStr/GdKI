from matplotlib import pyplot as plt
import pandas as pd

df = pd.read_csv('masie_4km_allyears_extent_sqkm.csv', header=1, delimiter=',')
dateList = df['yyyyddd']


def columnPicker():
    columnCounter = 0

    colorBlue = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
    colorRed = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1,1 ]
    alpha=[1,0.8,0.6,0.4,0.2,0.1,0.2,0.4,0.6,0.8,1]

    # For Schleife für Spalten aus DF
    for column in df:
        minList = []
        maxList = []
        secondPlot = []

        # >=1 da die Datum Spalte übersprungen wird und kleiner 18 da es nur 17 Spalten gibt
        if (columnCounter >= 1 and columnCounter < 18):
            print('Durchgang' + str(columnCounter))
            actColumn = df[column]

            # bringen der Zahlen ins richtige Zahlenformat damit Vergleich ermöglicht wird
            for j in range(1, 365):
                min = actColumn[j - 1]
                max = actColumn[j - 1]
                if (j < 10):
                    date = '00' + str(j)
                elif (j < 100):
                    date = '0' + str(j)
                else:
                    date = str(j)

                # fürs ablaufen aller Einträge in actColumn
                for z in range(0, len(actColumn)):
                    dateCompare = str(dateList[z])
                    # umformatieren in Format zum Vergleich. Bei nr 019 kam auch 2019 anstatt Tag 019
                    dateEquation = dateCompare[4:]

                    # Abfrage ob bearbeiteter Wert aus For Schleife in Einträgen der Spalte Datum ist
                    if (date in dateEquation):
                        # if any(str(j) in s for s in x):
                        if min > actColumn[z]:
                            min = actColumn[z]
                        if max < actColumn[z]:
                            max = actColumn[z]
                        secondPlot.append(actColumn[z])
                minList.append(min)
                maxList.append(max)
            plt.xlabel('Tage')
            plt.ylabel('SQKM')
            plt.plot(maxList, color='blue', label='Maximum')
            plt.plot(minList, color='green', label='Minimum')
            plt.legend()
            plt.show()

            #Farbverlauf klappt nur macht immer ein Plot komplett einfarbig
            #plt.plot(secondPlot, color=(colorBlue[columnCounter-1],0,colorRed[columnCounter-1],alpha[columnCounter-1]))
            plt.plot(secondPlot)

            plt.show()

            ##seasonal Plot




        elif (columnCounter >= 18):
            print(minList)
            print(maxList)
            break;
        columnCounter = columnCounter + 1


columnPicker()


def plotSeasonal():
    for j in range(1, 365):
        if (j < 10):
            date = '00' + str(j)
        elif (j < 100):
            date = '0' + str(j)
        else:
            date = str(j)
