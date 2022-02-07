#Importe
# ---------------------
import pandas as pd
import math
from matplotlib import pyplot as plt
import numpy as np
# ---------------------

# Dataframe der heruntergeladenen MASIE-NH Daten im .csv Format
df = pd.read_csv('masie_4km_allyears_extent_sqkm.csv', header=1, delimiter=',')

# funktion getName welche die Zahlen und zeichen wie z.B. (1) vor den Regionen entfernt
def getName(name):
    liste = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    while (name[0] == ' ' or name[0] == '(' or name[0] == ')' or name[0] in liste):
        name = name[1:]
    return name

# Funktion welche den moving Average einer Liste (hier einer Spalte) ausrechnet und zurückgibt
# window = 30, kommt aus Aufgabenstellung
def mvgAvg(liste, window=30):
    # Eine Liste für die durchschnitte
    avg = []
    # Start und Endpunkt für die 2. for-Schleife zuweisen
    start = math.floor(window / 2)
    end = len(liste) - start
    # For Schleife von 0 bis zum Wert von end
    for i in range(end):
        if i >= start:
            value = 0
            # for Schleife zum berechnen des moving averages
            for j in range(i - start, i + start + 1):
                value = value + liste[j]
            value = value / window
            # for schleife in Liste einfügen
            avg.append(value)
    return avg


def start(df):
    for column in df:
        # Datumsangabe ignorieren
        if column != 'yyyyddd':
            # Aktive Spalte zuweisen
            actColumn = df[column]
            # Durch die mvgAvg Funktion den aktuellen Durchschnittswert zuweisen
            avg = mvgAvg(actColumn)
            # Name der Spalte formatieren
            name = getName(column)
            # Titel, X und Y Achse benennen
            plt.title(name)
            plt.xlabel('Jahr')
            plt.ylabel('SQKM')
            # funktion zum näheren bennen der X Achse
            plt.xticks(np.arange(0, len(actColumn), 365.0),
                       ['06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21',
                        '22'])
            # Farbe der Zahlen der spalte in Blau
            plt.plot(actColumn, color='blue')
            # Farbe der Durchschnittswerte in Rot
            plt.plot(avg, color='red')
            plt.show()

# Startet das Skript
start(df)