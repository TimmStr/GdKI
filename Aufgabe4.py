import math

import pandas as pd
import warnings
from matplotlib import pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.arima_model import ARIMA

warnings.filterwarnings("ignore")

df = pd.read_csv("masie_4km_allyears_extent_sqkm.csv", header=1, delimiter=',')

def checkForStationary(ice, datelist):
    data = pd.DataFrame(list(zip(datelist, ice))).set_index(0)[1]
    plt.title("Starting Data")
    plt.plot(data)
    plt.show()
    print(df.columns)

    # AD Fuller test
    print("1. AD Fuller test")
    result = adfuller(data.values)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    plot_acf(data)
    plot_pacf(data)
    plt.show()

    # Ergebnis statistisch noch nicht relevant
    while result[1] > 0.05:
        print("Data was not stationary.")
        # diff data to make it stationary
        data = data.diff(periods=3)
        # AD Fuller test
        print("AD Fuller test")
        result = adfuller(data.values)
        print('ADF Statistic: %f' % result[0])
        print('p-value: %f' % result[1])
        plot_acf(data)
        plot_pacf(data)
        plt.show()
        plt.title("Stationary Data")
        plt.plot(data)
        plt.show()

    print("Data was stationary.")

def getName(name):
    liste=['0','1','2','3','4','5','6','7','8','9']
    while (name[0] == ' ' or name[0] == '(' or name[0] == ')'or name[0] in liste):
        name = name[1:]
    return name

def start(df):
    columnCounter = 0
    dateList = df['yyyyddd']
    for column in df:
        if (columnCounter >= 1 and len(df.columns)):
            name = getName(column)
            actColumn = df[column]
            checkForStationary(actColumn, dateList, name)
        elif (columnCounter >= 18):
            break;
        columnCounter = columnCounter + 1

start(df)