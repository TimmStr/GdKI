#!/usr/bin/env python
# coding: utf-8

# Prophet
# Quelle: https://medium.com/@cdabakoglu/time-series-forecasting-arima-lstm-prophet-with-python-e73a750a9887
# https://facebook.github.io/prophet/docs/quick_start.html

# If you have problems installing prophet use this tutorial
# https://medium.com/data-folks-indonesia/installing-fbprophet-prophet-for-time-series-forecasting-in-jupyter-notebook-7de6db09f93e

import pandas as pd
from datetime import datetime
import warnings

# there are often errors when installing prophet in pycharm
# if its not working set up anaconda-env (only tested in jupyter)
from prophet import Prophet

warnings.filterwarnings("ignore")

# converting date from 'yyyyddd' to 'yyyy-mm-dd'
def formatDate(dateList):
    formattedDateList = list()
    # format date from yyyyddd to yyyy-mm-dd
    for date in dateList:
        parsed = datetime.strptime(str(date), '%Y%j')
        formattedDateList.append(datetime.strftime(parsed, '%Y-%m-%d'))
    return formattedDateList

# calculate prophet for all regions - hard coded years 2006 - 2019, predict 2020
def prophet_all(data):
    for column in data:
        if column != 'yyyyddd':
            df_pr = data[['yyyyddd', column]]
            # filter years - from 2006 - 2019
            df_pr = df_pr.iloc[:5114]
            # format columns for prophet
            df_pr.columns = ['ds', 'y']
            df_pr['ds'] = formatDate(df_pr['ds'])
            # init prophet-model and train with dataframe
            m = Prophet()
            m.fit(df_pr)
            # build future-dataframe
            future = m.make_future_dataframe(periods=365)
            # make forecast based on future-dataframe
            forecast = m.predict(future)
            # plot forecast of 2020
            print('Plot for: '+str(column))
            fig1 = m.plot(forecast,xlabel='Year',ylabel='SQKM')
            fig1.show()
            # plot seasonal components of dataset
            fig2 = m.plot_components(forecast)
            fig2.show()
            # print forecast as table data
            print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

# change header to 1 when you are using jupyter
df = pd.read_csv('masie_4km_allyears_extent_sqkm.csv', header=1, delimiter=',')


# call prophet for all regions
prophet_all(df)