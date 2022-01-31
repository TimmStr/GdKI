from statsmodels.tsa.arima_model import ARIMA
from matplotlib import pyplot as plt
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv('masie_4km_allyears_extent_sqkm.csv', header=1, delimiter=',')
df2=df[' (0) Northern_Hemisphere']

def getName(name):
    liste=['0','1','2','3','4','5','6','7','8','9']
    while (name[0] == ' ' or name[0] == '(' or name[0] == ')'or name[0] in liste):
        name = name[1:]
    return name

def doArima(column,name):
    model = ARIMA(column, order=(3,1,2))
    results = model.fit(disp=-1)
    # given data
    plt.plot(column)
    # estimated differences
    plt.plot(results.fittedvalues, color='red')
    plt.title(name)
    # cumulated sum = prediction for time series
    predictions = results.fittedvalues.cumsum()
    plt.plot(predictions)
    plt.show()

    results.plot_predict(1,6000)
    plt.title(name)
    plt.show()

def start(df):
    columnCounter = 0
    dateList = df['yyyyddd']
    for column in df:
        if (columnCounter >= 1 and columnCounter<len(df.columns)):
            name=getName(column)
            actColumn = df[column]
            doArima(actColumn,name)
        elif (columnCounter >= 18):
            break;
        columnCounter = columnCounter + 1
start(df)
