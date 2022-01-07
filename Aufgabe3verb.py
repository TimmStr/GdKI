from matplotlib import pyplot as plt
import pandas as pd

df = pd.read_csv('masie_4km_allyears_extent_sqkm.csv', header=1, delimiter=',')
dateList = df['yyyyddd']

def columnPicker():
    columnCounter = 0

    # For Schleife für Spalten aus DF
    for column in df:
        minList = []
        maxList = []

        #>=1 da die Datum Spalte übersprungen wird und kleiner 18 da es nur 17 Spalten gibt
        if (columnCounter >= 1 and columnCounter < 18):
            print('Durchgang' + str(columnCounter))
            actColumn = df[column]

            #bringen der Zahlen ins richtige Zahlenformat damit Vergleich ermöglicht wird
            for j in range(1, 365):
                min = actColumn[j-1]
                max = actColumn[j-1]
                if (j < 10):
                    date = '00' + str(j)
                elif (j < 100):
                    date = '0' + str(j)
                else:
                    date = str(j)

                #fürs ablaufen aller Einträge in actColumn
                for z in range(0, len(actColumn)):
                    dateCompare = str(dateList[z])
                    dateEquation = dateCompare[4:]

                    #Abfrage ob bearbeiteter Wert aus For Schleife in Einträgen der Spalte Datum ist
                    if (date in dateEquation):
                        # if any(str(j) in s for s in x):
                        if min > actColumn[z]:
                            min = actColumn[z]
                        if max < actColumn[z]:
                            max = actColumn[z]
                minList.append(min)
                maxList.append(max)
            plt.xlabel('Tage')
            plt.ylabel('SQKM')
            plt.plot(minList,color='green')
            plt.plot(maxList,color='blue')
            plt.show()
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

