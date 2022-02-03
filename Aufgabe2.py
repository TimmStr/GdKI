import pandas as pd
import csv
from LoadData import pullMasie

# pullMasie zieht den Masie Datensatz
pullMasie()
df = pd.read_csv('masie_4km_allyears_extent_sqkm.csv', header=1, delimiter=',')


# ist für das einfügen der neuen Zeile in die Csv Datei zuständig
# counter steht für den Index an dem die row eingefüt werden soll
def csvInserter(counter, row):
    with open('masie_4km_allyears_extent_sqkm.csv', 'r', newline='\n') as readFile:
        reader = csv.reader(readFile)
        lines = list(reader)
        lines.insert(counter, row)
    with open('masie_4km_allyears_extent_sqkm.csv', 'w', newline='\n') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    readFile.close()
    writeFile.close()


# erstellen der Vergleichsliste (2006001, 2006002, ..., 2021365)
def createCompareList():
    compareList = []

    for y in range(2006, 2021):
        for d in range(1, 366):
            if (d < 10):
                date = '00' + str(d)
            elif (d < 100):
                date = '0' + str(d)
            else:
                date = str(d)
            date = str(y) + str(date)
            compareList.append(date)
    return compareList


# Hauptmethode des Programms
def insertNumbers(dateList, df):
    # Vergleichsliste
    compareList = createCompareList()
    indexCounter = 0
    addedValues = 0

    for i in range(0, len(compareList)):
        # dateCompare iteriert über ganzen Vergleichsliste und zieht immer das jeweilige Datum zum Vergleich raus
        dateCompare = str(compareList[indexCounter])
        # vergleicht ob das Datum in df[yyyyddd] ist, falls nicht geht er in den if teil
        if (dateCompare not in dateList):
            print('fehlender Wert: ' + str(dateCompare))
            row = []
            # iteriert über alle Spalten
            for column in df:
                vierTageDurchschnitt = 0
                # df[column] als liste speichern, da sonst kein Zugriff auf index möglich ist (wird bei for j Schleife wichtig)
                dfAlsListe = df[column].tolist()
                # wenn es die yyyyddd Spalte ist, fügt er row einfach das datum an. row wird benötigt für die Übergabe an csv Methode
                if (column == 'yyyyddd'):
                    row.append(dateCompare)
                else:
                    # for schleife über 4  Einträge in df (2 vor dem fehlenden, 2 nach dem fehlenden)
                    for j in range(-2, 2):
                        test = (i + j) - addedValues
                        # er bildet die Summe aus den 4 Werten der jeweiligen Spalte
                        zeile = dfAlsListe[i + j - addedValues]
                        vierTageDurchschnitt = vierTageDurchschnitt + zeile
                    # Summe von eben durch 4 teilen
                    mean_df = vierTageDurchschnitt / 4
                    gerundet = round(mean_df, 2)
                    row.append(str(gerundet))
            # Aufruf der MEthode zum modfizieren der Csv Datei. IndexCounter + 2 da ersten zwei Zeilen BEschriftung sind
            csvInserter(indexCounter + 2, row)
            indexCounter = indexCounter + 1
            # addedValues gibt an, wieviele Werte ersetzt wurden
            addedValues = addedValues + 1
        else:
            indexCounter = indexCounter + 1
    print('Fehlende Werte: ' + str(addedValues))


def start():
    insertNumbers(df['yyyyddd'].apply(str).tolist(), df)


start()
