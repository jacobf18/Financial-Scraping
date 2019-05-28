import urllib.request
import numpy as np
import pandas as pd
from pandas_datareader import data
from datetime import datetime
from datetime import timedelta

dataframe = pd.read_csv("dates_approval.csv")
comps = dataframe['Name']
dates = dataframe['Date']

print(len(comps), len(dates))
# Loop over all values
for i in range(len(comps)):
    current_date = datetime.utcfromtimestamp(dates[i]).strftime('%Y-%m-%d')
    start_date = datetime.utcfromtimestamp(dates[i]) - timedelta(days=7)
    end_date = datetime.utcfromtimestamp(dates[i]) + timedelta(days=7)
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    print(i, comps[i], start_date, end_date)
    try:
        panel_data = data.DataReader(comps[i], 'yahoo', start_date, current_date)
        panel_data.to_csv('equities/before/' + comps[i] + '_' + str(i) + '.csv')
        panel_data = data.DataReader(comps[i], 'yahoo', current_date, end_date)
        panel_data.to_csv('equities/after/' + comps[i] + '_' + str(i) + '.csv')
    except:
        continue
