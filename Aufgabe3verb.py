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
                    yearEquation = dateCompare[:4]

                    # Abfrage ob bearbeiteter Wert aus For Schleife in Einträgen der Spalte Datum ist
                    if (date in dateEquation):
                        if min > actColumn[z]:
                            min = actColumn[z]
                        if max < actColumn[z]:
                            max = actColumn[z]
                minList.append(min)
                maxList.append(max)
            plt.xlabel('Tage')
            plt.ylabel('SQKM')
            plt.plot(maxList, color='blue', label='Maximum')
            plt.plot(minList, color='green', label='Minimum')
            plt.legend()
            plt.show()


        elif (columnCounter >= 18):
            print(minList)
            print(maxList)
            break;
        columnCounter = columnCounter + 1


#columnPicker()





def plotSeasonal():
    colorBlue = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,0,0]
    colorRed = [0, 0, 0, 0, 0, 0,0,0, 1, 1, 1, 1, 1, 1,1,1]
    colorAlpha = [1,0.9, 0.8, 0.6, 0.4,0.3, 0.2, 0.1, 0.2,0.3, 0.4, 0.6, 0.8, 0.9, 1,1]
    columnCounter = 0
    # For Schleife für Spalten aus DF
    for column in df:
        # >=1 da die Datum Spalte übersprungen wird und kleiner 18 da es nur 17 Spalten gibt
        if (columnCounter >= 1 and columnCounter < 18):
            print('Durchgang' + str(columnCounter))
            actColumn = df[column]
            colorCounter=0

            # bringen der Zahlen ins richtige Zahlenformat damit Vergleich ermöglicht wird
            for j in range(2006, 2021):
                secondPlot = []
                colorCounter=colorCounter+1

                # fürs ablaufen aller Einträge in actColumn
                for z in range(0, len(actColumn)):
                    dateCompare = str(dateList[z])
                    # umformatieren in Format zum Vergleich. Jahr
                    yearEquation = dateCompare[:4]

                    # Abfrage ob bearbeiteter Wert aus For Schleife in Einträgen der Spalte Datum ist
                    if (str(j) in yearEquation):
                        secondPlot.append(actColumn[z])
                plt.title('Column: '+str(columnCounter))
                plt.xlabel('Tage')
                plt.ylabel('SQKM')
                plt.plot(secondPlot, label=str(j),
                         color=(colorBlue[colorCounter], 0, colorRed[colorCounter], colorAlpha[colorCounter]))

            plt.legend()
            plt.show()
        elif (columnCounter >= 18):
            break;
        columnCounter = columnCounter + 1


plotSeasonal()
