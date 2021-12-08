import pandas as pd
import math

df = pd.read_csv('masie_1km_allyears_extent_sqkm.csv', header=1)
x = df['yyyyddd']
z = df[' (0) Northern_Hemisphere'].values.tolist()


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
avg = mvgAvg(z)


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


x2 = dropper(x.values.tolist())

from matplotlib import pyplot as plt

plt.plot(x, z)
plt.xlabel('Month')
plt.title('ohne mvg')
plt.show()


#plt.plot(x2,avg)
plt.plot( avg, color='red')
plt.xlabel('Month')
plt.title('mit Mvg')
plt.show()
