import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    dataframe = pd.read_csv('volatility.csv')
    before_sd = dataframe['Before Standard Deviation']
    full_sd = dataframe['Full Standard Deviation']
    difference_sd = []
    for i, val in enumerate(before_sd):
        difference_sd.append(abs(val - full_sd[i]))
    dataframe.insert(4, 'Difference', difference_sd, True)

    # Plot diff vs market cap
    market_caps = dataframe['Market Cap']
    fig1 = plt.figure(1)
    plt.scatter(market_caps, difference_sd)
    plt.xlabel('Market Caps')
    plt.ylabel('Volatility Difference')

    # Plot diff vs original volatility
    fig2 = plt.figure(2)
    plt.scatter(before_sd, difference_sd)
    plt.xlabel('Original Volatility')
    plt.ylabel('Volatility Difference')

    # Plot diff vs after volatility
    fig3 = plt.figure(3)
    plt.scatter(full_sd, difference_sd)
    plt.xlabel('Full Volatility')
    plt.ylabel('Volatility Difference')

    plt.show()
