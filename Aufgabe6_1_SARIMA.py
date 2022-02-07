from pmdarima import auto_arima
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import kpss
from matplotlib import pyplot as plt
import pandas as pd
import math
import warnings
from statsmodels.tsa.stattools import adfuller
from datetime import datetime

warnings.filterwarnings("ignore")

def performAutoArima(data):
    result = auto_arima(data, seasonal=True, m=12, max_p=7,
               max_d=5, max_q=7, max_P=4, max_D=4,
               max_Q=4).summary()
    print(result)

def getName(name):
    liste=['0','1','2','3','4','5','6','7','8','9']
    while (name[0] == ' ' or name[0] == '(' or name[0] == ')'or name[0] in liste):
        name = name[1:]
    return name

def differencBySeasonality(data, period):
    return data.diff(period).dropna()

def kpss_test(timeseries):
    print("Results of KPSS Test:")
    kpsstest = kpss(timeseries, regression="c", nlags="auto")
    kpss_output = pd.Series(
        kpsstest[0:3], index=["Test Statistic", "p-value", "Lags Used"]
    )
    for key, value in kpsstest[3].items():
        kpss_output["Critical Value (%s)" % key] = value
    print(kpss_output)

def adFullerTest(data):
    result = adfuller(data, autolag="AIC")
    print('ADF Statistic: %f' % result[0])
    print('p-value from adf: %f' % result[1])
    return result[1]

def plotDataWithMean(data):
    # plot data with mean
    plt.plot(data)
    plt.axhline(y=data.values.mean(), color='r', linestyle='-')
    plt.show()

def forecastAnalysisByColumn(data, name):
    # visualize data first with mean
    plotDataWithMean(data)

    # use KI to get best values for SARIMA-Modell (p, d, q) and (P , D, Q)
    # performAutoArima(data)

    # check if data is stationary (adFuller, kpss) and diff if not
    data, d = makeDataStationaryByDiff(data)

    # plot acf and pacf from data
    plot_acf(data, lags= 80)
    plot_pacf(data, lags= 36)
    plt.show()

    # perform SARIMA - print result and retrieve data
    # p, q, d as order of Autoregression,
    # Integration and MA terms for non-seasonal and seasonal component
    # enter all number including d manually if you are using auto_arima
    forecast, train, test = performSARIMA(data, 12, 14/15,
                                          p=4, d=d, q=0, P=3, D=0, Q=0)

    # plot trained model with forecast
    plt.plot(forecast)
    plt.title(name)
    plt.xlabel('Year')
    plt.ylabel('Ice')
    plt.show()

    # Plot der Trainingsdaten, forecast und Testdaten
    plt.plot(train, color = 'blue')
    plt.plot(forecast, color = 'black')
    plt.plot(test, color = 'red')
    plt.title(name)
    plt.xlabel('Year')
    plt.ylabel('Ice')
    plt.show()

def filterDateListByYear(dateList, fromYear, toYear):
    filteredDates = list()
    for j in range(fromYear, toYear):
        # fürs ablaufen aller Einträge in dateList
        for date in dateList:
            dateCompare = str(date)
            # umformatieren in Format zum Vergleich (year)
            yearEquation = dateCompare[:4]
            # Abfrage ob bearbeiteter Wert aus For Schleife
            # in Einträgen der Spalte Datum ist
            if (str(j) in yearEquation):
                filteredDates.append(formatDate(date, '%Y-%m-%d'))
    return filteredDates

def formatDate(date, format):
    parsed = datetime.strptime(str(date), '%Y%j')
    return datetime.strftime(parsed, format)

def makeDataStationaryByDiff(data):
    # set integration count for SARIMA (Integration)
    countOfIntegration = 0
    # pValue > 0.05 - Ergebnis statistisch noch nicht relevant
    # adFullerTest returns pValue
    # perform till stationary
    while adFullerTest(data) > 0.05:
        print("Data was not stationary.")
        # diff data to make data seasonal stationary 12 = months
        # data = data.diff(12).dropna()
        # diff to make data trend stationary
        data = data.diff().dropna()
        countOfIntegration = countOfIntegration+1
    # double check with kpss - desired result = 0.1
    kpss_test(data)
    plt.title("Stationary Data")
    plt.axhline(y=data.values.mean(), color='r', linestyle='-')
    plt.plot(data)
    plt.show()
    return data, countOfIntegration

# seasonalFactor euqals m
def performSARIMA(data, seasonalFactor, splitFactor, p, d, q, P, D, Q):
    # n*splitFactor - 14/15 für 2006-2019 training und 2020 test
    n = len(data)
    train_split = math.floor(n * splitFactor)
    # split into train and test data
    train = data[:train_split]
    test = data[train_split:n]
    # train SARIMA-Model
    # p, q, d as order of Autoregression, Integration
    # and MA terms for non-seasonal and seasonal component
    model = SARIMAX(train, order=(p, d, q),
                    seasonal_order=(P, D, Q, seasonalFactor))
    results = model.fit()
    # print result (model and training)
    print(results.summary())
    # acutal forecast with sarima
    # seasonaFactor m for 12 Months equals forecast till end of 2020
    forecast = results.predict(1, n + seasonalFactor)
    return forecast, train, test

def start(df):
    # filter dateList and format
    dateList = filterDateListByYear(df['yyyyddd'], 2006, 2020)
    for column in df:
        if column != 'yyyyddd':
            name = getName(column)
            actColumn = df[column]
            # build new dataFrame for each dataset
            data = pd.DataFrame(actColumn.values[:len(dateList)],
                            index=pd.to_datetime(dateList), columns=['Ice'])
            # resample data for analysis
            # Q = Quarterly, M = Monthly, W = Weekly
            data = data.resample('M').mean().dropna()
            # apply SARIMA analysis for each new dataset
            forecastAnalysisByColumn(data, name)


# read csv into a dataframe
df = pd.read_csv('masie_4km_allyears_extent_sqkm.csv', header=1, delimiter=',')

start(df)