import pandas as pd
import numpy as np
import os


def calculate_sd(prices):
    percent_changes = []
    for i, val in enumerate(prices):
        if i > 0:
            percent_change = 100 * (val - prices[i-1])/prices[i-1]
            percent_changes.append(percent_change)
    return np.std(np.array(percent_changes))

if __name__ == '__main__':
    before_sd = []
    full_sd = []
    pc = []
    file_names = []

    before_close_prices_dict = {}
    market_caps = []

    directory = os.fsencode('equities/before/')
    for file in os.listdir(directory):
        filename = os.fsencode(file)
        file_names.append(filename)
        full_path = os.path.join(directory, filename).decode('utf-8')
        dataframe = pd.read_csv(full_path)
        before_close_prices = dataframe['Close'].tolist()
        before_close_prices_dict[filename] = before_close_prices
        sd = calculate_sd(before_close_prices)
        before_sd.append(sd)
        market_caps.append(dataframe['Market Cap'].tolist()[0])

    directory = os.fsencode('equities/after/')
    for file in os.listdir(directory):
        filename = os.fsencode(file)
        full_path = os.path.join(directory, filename).decode('utf-8')
        dataframe = pd.read_csv(full_path)
        after_close_prices = dataframe['Close'].tolist()
        bc = before_close_prices_dict[filename][-1]
        before_close_prices_dict[filename].extend(after_close_prices)
        sd = calculate_sd(before_close_prices_dict[filename])
        full_sd.append(sd)
        pc.append(abs(after_close_prices[-1] - bc))

    for i, val in enumerate(file_names):
        file_names[i] = val.decode('utf-8')
        index = file_names[i].find('.csv')
        file_names[i] = file_names[i][:index]

    dataframe = pd.DataFrame({
        'Name': file_names,
        'Before Standard Deviation': before_sd,
        'Full Standard Deviation': full_sd,
        'Change': pc,
        'Market Cap': market_caps
        })
    print(dataframe)
    dataframe.to_csv('volatility.csv')
