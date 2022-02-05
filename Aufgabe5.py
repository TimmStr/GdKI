import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss
from matplotlib import pyplot as plt
from statsmodels.tsa.seasonal import STL
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf

# CreatePdf eigens erstellte Klasse
from CreatePdf import create
from CreatePdf import deleteFiles

# Einlesen der CSV Datei in ein Dataframe
df = pd.read_csv('masie_4km_allyears_extent_sqkm.csv', header=1, delimiter=',')


# Funktion zum umformatieren des Spaltennamen: "(0) Northern_Hemisphere" zu "Northern_Hemisphere"
def getName(name):
    # String Vergleichsliste
    liste = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    # wenn der erste Buchstabe aus einem der folgenden Zeichen
    # oder einem String aus der liste entspricht, wird das erste Zeichen ausgeschlossen
    while (name[0] == ' ' or name[0] == '(' or name[0] == ')' or name[0] in liste):
        name = name[1:]
    return name


# ADF Test wird für jede Region (Spalte) einzeln durchgeführt
def adf_test(column):
    # ADF Test aus dem Statsmodels Paket
    dftest = adfuller(column)
    # Ergebnis des Tests in einer Pandas Series (eine Art Liste) abspeichern
    dfoutput = pd.Series(dftest[0:4],
                         index=["Test Statistic", "p-value", "Lags Used", "Number of Observations Used", ], )
    # speziell für Critical Values, da diese in Form eines Dictionaries auf index 4 gespeichert werden
    for key, value in dftest[4].items():
        dfoutput["Critical Value (%s)" % key] = value
    # Rückgabewert ist die Pandas Series (eine Art Liste)
    return dfoutput


# KPSS Test wird für jede Region (Spalte) einzeln durchgeführt
def kpss_test(column):
    # KPSS Test aus dem Statsmodels Paket
    kpsstest = kpss(column, regression="ct", nlags="auto")
    # Ergebnis des Tests in einer Pandas Series (eine Art Liste) abspeichern
    kpss_output = pd.Series(
        kpsstest[0:3], index=["Test Statistic", "p-value", "Lags Used"]
    )
    # speziell für Critical Values, da diese in Form eines Dictionaries auf index 4 gespeichert werden
    for key, value in kpsstest[3].items():
        kpss_output["Critical Value (%s)" % key] = value
    # Rückgabewert ist die Pandas Series (eine Art Liste)
    return kpss_output


def stlDecomposition(column, name):
    # STL Decomposition aus dem Statsmodels Paket
    res = STL(column, period=365).fit()
    # plotten der Ergebnisse
    res.plot()
    # picName ist unter der die Grafik abgespeichert wird (relevant für die PDF Erstellung)
    picName = name + '.png'
    # abspeichern des Plots um während der PDF Erstellung darauf zugreifen zu können
    plt.savefig(picName)
    # plt.show() kann bei einmaligem Durchlauf auch auskommentiert werden
    # Bei mehrmaligem Durchlauf muss es aber drin bleiben, da es sonst zu Problemen mit der Scientific View kommt
    plt.show()


# Berechnung der Autocorrelation und der partiellen Autocorrelation
# Als Übergabewerte wird die aktuelle Region (Spalte) übergeben und der name für die Beschriftung des Plots
def calcAcf(column, name):
    # zusammensetzen der Spalte Datum und der aktuellen Spalte mit Wrten
    data = pd.DataFrame(list(zip(df['yyyyddd'], column))).set_index(0)[1]
    # Aufruf der Autocorrelationsfunktion aus dem Statsmodels Paket
    # lags werden über den gesamten Zeitraum dargestellt.
    plot_acf(data, lags=len(column) - 1)
    # title = Überschrift
    plt.title('Autocorrelation: ' + name)
    # xticks = x-Achsen Einteilung
    plt.xticks(np.arange(0, len(df) - 1, 365),
               ['06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22'])
    # filename = Name unter dem die Autokorrelationsgrafik abgespeichert wird (für PDF Erstellung)
    filename = name + '_autocorr.png'
    # xlabel=Beschritung der x-Achse
    plt.xlabel('Jahr')
    # abspeichern der Datei
    plt.savefig(filename)

    # Aufruf der partiellen Autokorrelationsfunktion aus dem Statsmodels Paket
    plot_pacf(data, lags=40, method='ywm')
    # filename ist der Dateiname der partiellen Autokorrelations Grafik
    filename = name + '_part_autocorr.png'
    # title = Überschrift
    plt.title('Partial Autocorrelation: ' + name)
    # abspeichern der partiellen Autokorrelationsgrafik unter filename (für PDF Erstellung)
    plt.savefig(filename)


def start():
    # for Schleife iteriert über alle Spalten im Dataframe
    for column in df:
        # Überprüfung ob die Spalte nicht die Datumsspalte ist
        # Grafiken plotten macht für die Datumsspalte keinen Sinn
        if column != 'yyyyddd':
            # Aufruf der getName Funktion um den Dateinamen in ein schöneres Format zu bringen
            name = getName(column)
            # Aufruf der ADF Funktion. Ergebnis wird in pdfAdf gespeichert
            pdfAdf = adf_test(df[column])
            # Aufruf der KPSS Funktion. Ergebnis wird in pdfKpss gespeichert
            pdfKpss = kpss_test(df[column])
            # Aufruf der STL-Decomposition mit der aktuellen Spalte und dem formatierten Namen
            stlDecomposition(df[column], name)
            # Aufruf der Autocorrelation und partiellen Autocorrelation Funktion
            calcAcf(df[column], name)
            # create Funktion stammt aus der eigens erstellten CreatePdf Klasse
            create(name, pdfAdf, pdfKpss)
            # delete Funktion stammt aus der eigens erstellten CreatePdf Klasse
            deleteFiles(name)


# Start des Programms
start()

