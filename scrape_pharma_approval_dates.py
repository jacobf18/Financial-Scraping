import urllib.request
import numpy as np
import pandas as pd

comp_names = []
dates = []
infos = []

if __name__ == '__main__':
    html = urllib.request.urlopen('https://www.biopharmcatalyst.com/calendars/historical-catalyst-calendar').read().decode("utf8")
    start_index = html.find('<main')
    start_index = html.find('<div class="table-wrap"', start_index)
    end_index = html.find('</main>')
    html = html[start_index:end_index]

    while len(html) > 0:
        name = ''
        date = 0
        info = ''
        if '<tr>' not in html:
            break
        start_index = html.find('<tr>', start_index)
        start_index = html.find('<td>', start_index)
        start_index = html.find('ticker', start_index)
        start_index = html.find('>', start_index)
        end_index = html.find('<', start_index)
        name = html[start_index+1:end_index]
        start_index = end_index+1
        for i in range(3):
            start_index = html.find('<td', start_index+1)
        start_index = html.find('data-value', start_index)
        start_index = html.find('"', start_index)
        end_index = html.find('"', start_index+1)
        date = int(html[start_index+2: end_index-1])
        start_index = html.find('class', start_index)
        start_index = html.find('>', start_index)
        end_index = html.find('<', start_index)
        info = html[start_index+1: end_index]
        if 'Approved' in info or 'approved' in info or 'crl' in info or 'CRL' in info:
            comp_names.append(name)
            dates.append(date)
            infos.append(info)
        html = html[start_index:]
        start_index = 0
    dataframe = pd.DataFrame({
        'Name': comp_names,
        'Date': dates,
        'Info': infos
        })
    dataframe.to_csv('dates_approval.csv')
