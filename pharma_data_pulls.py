#!/usr/bin/env python
# coding: utf-8

# In[36]:


from urllib.request import Request, urlopen, urlretrieve
from urllib.parse import urljoin
import requests
import os
import pandas as pd
import numpy as np

rootdir = 'C:/Users/minif/OneDrive/Desktop/'


# In[37]:


# Pulls HTML from biopharmcatalyst.com stock listings

def pull_html():
    try: 
        r = requests.get('https://www.biopharmcatalyst.com/calendars/historical-catalyst-calendar')
        
    except Exception :
        print("Request for html failed.")
        return

    if r.status_code == 200:
        r = Request('https://www.biopharmcatalyst.com/calendars/historical-catalyst-calendar'
                    , headers={'User-Agent': 'Chrome/67.0.3396.99'})

        u = urlopen(r)
        html = u.read().decode('utf-8')
        return html
    else:
        print("An HTTP Error has Occured. Error Code: "+str(r.status_code))
        


# In[49]:


# Pulls the dates of important dates in FDA approval phase

def get_dates_and_tickers(html):
    drug_date_list = []
    drug_date_unix_list = []
    drug_ticker_list = []
    
    if html == None:
        return "no data"
    
    while "class=\"ticker\"" in html:
        index = html.find("class=\"ticker\"")
        ticker = html[index+15:index+19]
        
        if "<" in ticker:
            ticker = ticker.replace("<", "")
        
        index = html.find("class=\"catalyst-date\"", index);
        unix_date = html[index+35:index+45]
        date = html[index+48:index+58]
        
        drug_date_unix_list.append(unix_date)
        drug_date_list.append(date)
        drug_ticker_list.append(ticker)
            
        html = html[index:]
            
    else:
        return [drug_ticker_list,drug_date_unix_list,drug_date_list]
            


# In[53]:


html_bio = pull_html()
pull_output = get_dates_and_tickers(html_bio)


# In[66]:


def write_dates_excel(data):
    df_output = pd.DataFrame({'Tickers': data[0], 'Catalyst Date': data[2], 'Unix Timestamp': data[1]})
    
    writer = pd.ExcelWriter('C:/Users/minif/OneDrive/Desktop/pharma_historical_dates.xlsx')
    df_output.to_excel(writer,'Sheet1')
    writer.save()
    
    return df_output


# In[67]:


write_dates_excel(pull_output)

