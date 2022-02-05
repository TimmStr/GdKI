# Quellen
# https://machinelearningmastery.com/remove-trends-seasonality-difference-transform-python/
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf
from matplotlib import pyplot as plt

df = pd.read_csv('masie_4km_allyears_extent_sqkm.csv', header=1, delimiter=',')

list_names=[]
list_mean_interv1=[]
list_mean_interv2=[]
list_mean_interv3=[]
list_var_interv1=[]
list_var_interv2=[]
list_var_interv3=[]



def calc_mean(column, start, end):
    return column.iloc[start:end + 1].mean()

def calc_var(column, start, end):
    return column.iloc[start:end+1].var()

def calc_intervall(column,intervall=5):
    start = 0
    end = start + intervall * 365
    for i in range(2006, 2021, intervall):
        if i == 2006:
            list_mean_interv1.append(calc_mean(df[column], start, end))
            list_var_interv1.append(calc_var(df[column], start, end))
        elif i == 2011:
            list_mean_interv2.append(calc_mean(df[column], start, end))
            list_var_interv2.append(calc_var(df[column], start, end))
        elif i ==2016:
            list_mean_interv3.append(calc_mean(df[column], start, end))
            list_var_interv3.append(calc_var(df[column], start, end))
        start = end + 1
        end = end + intervall * 365

def calc(df,lags=365,intervall=5):
    for column in df.iloc[:, 1:]:
        # calc_mean_var_for_single_years(df, column)
        plot_acf(df[column], lags=lags)
        plt.title(column)
        plt.show()
        calc_intervall(column,intervall)
def names(df):
    for column in df:
        if column!='yyyyddd':
            list_names.append(column)

def start():
    calc(df)
    names(df)
    i = 0
    for column in df:
        if i ==0:
            print()
            i=i+1
        else:
            print('Mittelwert für Region: '+list_names[i-1])
            print(list_mean_interv1[i-1])
            print(list_mean_interv2[i-1])
            print(list_mean_interv3[i-1])
            print('Varianz für Region: '+list_names[i-1])
            print(list_var_interv1[i-1])
            print(list_var_interv2[i-1])
            print(list_var_interv3[i-1])
            print()
            print()
            i = i + 1

    df_diff = df.diff().dropna()
    calc(df_diff)
start()