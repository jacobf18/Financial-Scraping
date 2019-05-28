import pandas as pd
import numpy as np
import os

if __name__ == '__main__':
    comps = []
    dates_begin = []
    dates_end = []

    directory = os.fsencode('equities/before/')
    for file in os.listdir(directory):
        filename = os.fsencode(file)
        full_path = os.path.join(directory, filename).decode('utf-8')
        dataframe = pd.read_csv(full_path)

        # Get comp name from filename
        index = filename.decode('utf-8').find('_')
        comps.append(filename.decode('utf-8')[:index])
        dates = dataframe['Date'].tolist()
        dates_begin.append(dates[0])
        dates_end.append(dates[-1])

    dataframe = pd.DataFrame({
        'Name': comps,
        'Date Begin': dates_begin,
        'Date End': dates_end
        })
    print(dataframe)
    dataframe.to_csv('comps_dates_testing.csv')
