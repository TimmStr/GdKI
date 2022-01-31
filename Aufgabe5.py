from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss
import pandas as pd
import numpy as np
df = pd.read_csv('masie_4km_allyears_extent_sqkm.csv', header=1, delimiter=',')


def getName(name):
    liste = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    while (name[0] == ' ' or name[0] == '(' or name[0] == ')' or name[0] in liste):
        name = name[1:]
    return name


def adf_test(timeseries):
    dftest = adfuller(timeseries, autolag="AIC")
    dfoutput = pd.Series(dftest[0:4],
                         index=["Test Statistic", "p-value", "#Lags Used", "Number of Observations Used", ], )
    # speziell für Critical Values
    for key, value in dftest[4].items():
        dfoutput["Critical Value (%s)" % key] = value
    return dfoutput


def kpss_test(timeseries):
    kpsstest = kpss(timeseries, regression="c", nlags="auto")
    kpss_output = pd.Series(
        kpsstest[0:3], index=["Test Statistic", "p-value", "Lags Used"]
    )
    for key, value in kpsstest[3].items():
        kpss_output["Critical Value (%s)" % key] = value
    return kpss_output


from matplotlib import pyplot as plt

from statsmodels.tsa.seasonal import STL


def stlDecomposition(timeseries, name):
    data = timeseries
    res = STL(data, period=365).fit()
    res.plot()
    picName = name + '.png'
    # for PDF
    plt.savefig(picName)
    plt.show()


from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf


def calcAcf(column, timeline, name):
    data = pd.DataFrame(list(zip(timeline, column))).set_index(0)[1]

    plot_acf(data,lags=5816)
    plt.title('Autocorrelation: ' + name)
    plt.xticks(np.arange(0,len(df)-1,365),
               ['06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22'])
    filename = name + '_autocorr.png'
    plt.xlabel('Jahr')
    plt.savefig(filename)

    plot_pacf(data,lags=40)
    filename = name + '_part_autocorr.png'
    plt.title('Partial Autocorrelation: ' + name)
    plt.savefig(filename)


from CreatePdf import create


def columnPicker():
    counter = 0
    date = df['yyyyddd']
    for column in df:
        if (counter >= 1 and counter < len(df.columns)):
            name = getName(column)

            pdfAdf = adf_test(df[column])

            pdfKpss = kpss_test(df[column])

            stlDecomposition(df[column], name)

            calcAcf(df[column], date, name)

            create(name, pdfAdf, pdfKpss)
        elif (counter >= 18):
            break
        counter = counter + 1


def start():
    columnPicker()



start()
