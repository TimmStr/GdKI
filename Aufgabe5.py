from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss
import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('masie_4km_allyears_extent_sqkm.csv', header=1, delimiter=',')



def getName(name):
    liste=['0','1','2','3','4','5','6','7','8','9']
    while (name[0] == ' ' or name[0] == '(' or name[0] == ')'or name[0] in liste):
        name = name[1:]
    return name

def adf_test(timeseries, name):
    print("Results of Dickey-Fuller Test for: " + name)
    dftest = adfuller(timeseries, autolag="AIC")
    dfoutput = pd.Series(dftest[0:4],
                         index=["Test Statistic", "p-value", "#Lags Used", "Number of Observations Used", ], )

    for key, value in dftest[4].items():
        dfoutput["Critical Value (%s)" % key] = value
    print(dfoutput)
    print()
    # for PDF
    return dfoutput


def kpss_test(timeseries, name):
    print("Results of KPSS Test for: " + name)
    kpsstest = kpss(timeseries, regression="c", nlags="auto")
    kpss_output = pd.Series(
        kpsstest[0:3], index=["Test Statistic", "p-value", "Lags Used"]
    )
    for key, value in kpsstest[3].items():
        kpss_output["Critical Value (%s)" % key] = value
    print(kpss_output)
    print()
    #for PDF
    return kpss_output


from matplotlib import pyplot as plt

from statsmodels.tsa.seasonal import STL
def stlDecomposition(timeseries,name):
    data=timeseries
    res=STL(data,period=365).fit()
    res.plot()
    picName=name+'.png'
    #for PDF
    plt.savefig(picName)
    plt.show()



from statsmodels.tsa.stattools import acf
def columnPicker():
    counter = 0
    for i in df:
        if (counter >= 1 and counter < 18):
            name=getName(i)
            column = df[i]
            pdfAdf=adf_test(column, name)
            pdfKpss=kpss_test(column,name)
            stlDecomposition(column,name)
            print()
            print("Autocorrelation for column:"+str(counter))
            pdfAcf=acf(column)
            print(pdfAcf)
        elif (counter >= 18):
            break;
        counter = counter + 1


from CreatePdf import startPdf
def start():
    columnPicker()
    startPdf(df)



start()