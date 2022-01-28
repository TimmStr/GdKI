import pandas as pd
import csv

df = pd.read_csv('masie_4km_allyears_extent_sqkm.csv', header=1, delimiter=',')


def csvInserter(counter, row):
    with open('masie_4km_allyears_extent_sqkm.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        lines = list(reader)
        lines.insert(counter, row)
    with open('masie_4km_allyears_extent_sqkm.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    readFile.close()
    writeFile.close()


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


def insertNumbers(dateList, df):
    compareList = createCompareList()
    indexCounter = 0
    addedValues = 0

    for i in range(0, len(compareList) - 1):
        dateCompare = str(compareList[indexCounter])
        if (dateCompare not in dateList):
            print(dateCompare)
            row = []
            for column in df:
                if (column == 'yyyyddd'):
                    row.append(dateCompare)
                else:
                    mean_df = df[column].mean()
                    gerundet = round(mean_df, 2)
                    row.append(str(gerundet))
            print(str(dateCompare) + ' dateCompare')
            csvInserter(indexCounter + 2, row)
            indexCounter = indexCounter + 1
            addedValues = addedValues + 1
        else:
            indexCounter = indexCounter + 1
    print('Fehlende Werte: ' + str(addedValues))


def start():
    insertNumbers(df['yyyyddd'].apply(str).tolist(), df)
start()
