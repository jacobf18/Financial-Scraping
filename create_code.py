import pandas as pd
import numpy as np
import os

dataframe = pd.read_csv('comps_dates_testing.csv')
comps = dataframe['Name'].tolist()
comps_new = list(dict.fromkeys(comps))

for n in comps_new:
    print('self.AddOption("' + n + '", Resolution.Minute)')
