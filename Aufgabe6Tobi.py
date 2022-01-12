from statsmodels.tsa.arima_model import ARIMA
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.metrics import mean_squared_error
import math
import numpy as np
import warnings
warnings.filterwarnings("ignore")


"""
Still missing:
-> Correct Labeling for data
-> Only Range from 2006 to 2019
Bugs:
-> Can only forecast one column - then error "TypeError: 'numpy.ndarray' object is not callable" at line 54
-> Workaround is switching columns manually in line 77
"""

# read csv into a dataframe
df = pd.read_csv('masie_4km_allyears_extent_sqkm.csv', header=1, delimiter=',')

# order of autoregression
p=3
# order of integration (defferences)
d=1
# Order of MA terms
q=2

splitFactor=2/3

def getName(name):
    liste=['0','1','2','3','4','5','6','7','8','9']
    while (name[0] == ' ' or name[0] == '(' or name[0] == ')'or name[0] in liste):
        name = name[1:]
    return name

def plotArimaByColumn(data,name):
    n = len(data)
    train_split = math.floor(n * splitFactor)
    numOfValidates = n - train_split

    # split into train and test data
    train = data[:train_split]
    test = data[train_split:]

    print(n, len(train), len(test))

    model = ARIMA(train, order=(p, d, q))
    results = model.fit(disp=-1)

    print(results.summary())
    results.plot_predict(1, n)
    plt.title(name)
    plt.show()

    forecast = results.forecast(steps=numOfValidates)[0]
    #print("Means Squared Error:", mean_squared_error(forecast(test)))

    # Plot der Trainingsdaten mit forecast
    plt.plot(np.append(train.values, forecast))
    plt.title(name)
    plt.show()

    # Plot der Testdaten
    plt.plot(data)
    plt.title(name)
    plt.show()

def start(df):
    columnCounter = 0
    for column in df:
        if (columnCounter >= 1 and len(df.columns)):
            name = getName(column)
            actColumn = df[column]
            plotArimaByColumn(actColumn,name)
        elif (columnCounter >= 18):
            break;
        columnCounter = columnCounter + 1

start(df)
