from matplotlib import pyplot as plt
import pandas as pd

df = pd.read_csv('masie_1km_allyears_extent_sqkm.csv', header=1, delimiter=',')
x = df['yyyyddd']

def useColumns():
    counter = 0
    dayList = []
    minList = []
    maxList = []
    # For Schleife für Spalten aus DF
    for column in df:
        if (counter >= 1 and counter < 18):
            print('Durchgang' + str(counter))
            actColumn = df[column]
            for j in range(1, 365):
                if (j < 10):
                    date = '00' + str(j)
                elif (j < 100):
                    date = '0' + str(j)
                else:
                    date = str(j)

                dayList.append(j)
                min = actColumn[0]
                max = actColumn[0]
                for z in range(0, len(actColumn)):
                    dateCompare = str(x[z])
                    if (str(j) in dateCompare):
                        # if any(str(j) in s for s in x):
                        if min > actColumn[z]:
                            min = actColumn[z]
                        if max < actColumn[z]:
                            max = actColumn[z]
                minList.append(min)
                maxList.append(max)
            plt.plot(minList,color='green')
            plt.plot(maxList,color='blue')
            plt.show()


        elif (counter >= 18):
            print(minList)
            print(maxList)
            break;
        counter = counter + 1


useColumns()
"""
liste=['xyz','zys','zzz']
for i in liste:
    z=str(i)
    if 'z'in z:
        print(z)
"""

