import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf
from matplotlib import pyplot as plt

# read csv-data in dataframe
df = pd.read_csv('masie_4km_allyears_extent_sqkm.csv', header=1, delimiter=',')

# define lists for names and intervals 1-3
list_names = []

# 3 intervals for mean
list_mean_interv1 = []
list_mean_interv2 = []
list_mean_interv3 = []

# 3 intervals for variance
list_var_interv1 = []
list_var_interv2 = []
list_var_interv3 = []


# calculate mean
def calc_mean(column, start, end):
    return column.iloc[start:end + 1].mean()

# calculate variance
def calc_var(column, start, end):
    return column.iloc[start:end+1].var()

# function calls calc_mean and calc_var and appends values to specific interval-lists
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

# plots acf-plots and call calc_intervall
def calc(df,lags=365,intervall=5):
    for column in df.iloc[:, 1:]:
        # plot acf-plot
        plot_acf(df[column], lags=lags)
        plt.title(column)
        plt.show()

        # call calc_intervall to perform mean/var caluclations
        calc_intervall(column,intervall)

# get columns names and append to list_names
def names(df):
    for column in df:
        if column!='yyyyddd':
            list_names.append(column)

# start function: calls other functions and runs whole program
def start():
    calc(df)
    names(df)
    i = 0
    for column in df:
        if i == 0:
            print()
            i = i + 1
        else:
            print('Mittelwert für Region: '+ list_names[i-1])
            print(list_mean_interv1[i-1])
            print(list_mean_interv2[i-1])
            print(list_mean_interv3[i-1])
            print('Varianz für Region: '+ list_names[i-1])
            print(list_var_interv1[i-1])
            print(list_var_interv2[i-1])
            print(list_var_interv3[i-1])
            print()
            print()
            i = i + 1

# call start-function and run whole program
start()