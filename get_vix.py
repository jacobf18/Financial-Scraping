import urllib.request
import numpy as np
import pandas as pd
from pandas_datareader import data
from datetime import datetime
from datetime import timedelta

start_date = "1/2/1990"
end_date = "6/11/2019"
panel_data = data.DataReader('^VIX', 'yahoo', start_date, end_date)
panel_data.to_csv('VIX.csv')
