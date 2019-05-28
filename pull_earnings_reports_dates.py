#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from urllib.request import Request, urlopen, urlretrieve
from urllib.parse import urljoin
import requests
import re
import os
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
from datetime import date

'''
    This script pulls earnings reports dates from Market Chameleon using the hyperlinks.
    It runs through every date from the start date to the end date.
    It returns an excel spreadsheet with the data.
'''
final_output = {
    'Ticker': [],
    'Name': [],
    'Date': [],
    'Time': [],
    'Previous Move': [],
    'Expected Move': [],
    'This Move': [],
    'Options Volume': [],
    'Market Cap': []
}
start_date = [2018, 10, 1]
end_date = [2018, 10, 1]
dates = []

delay = 10 #seconds
browser = webdriver.Firefox()


# In[2]:


def format_date(dt):
    return datetime.strftime(dt, '%Y%m%d')


# In[3]:


def find_dates(year1, month1, day1, year2, month2, day2):
    d1 = date(year1, month1, day1)  # start date
    d2 = date(year2, month2, day2)  # end date

    delta = d2 - d1         # timedelta

    for i in range(delta.days + 1):
        dates.append(format_date(d1 + timedelta(i)))


# In[4]:


def pull_data(date_formatted):
    browser.get('https://marketchameleon.com/Calendar/Earnings?d=' + date_formatted)
    
    WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH('//option[@value="-1"]'))))
    
    num_btn = browser.find_element_by_xpath('//option[@value="-1"]')


# In[5]:


find_dates(start_date[0], start_date[1], start_date[2], end_date[0], end_date[1], end_date[2])
for d in dates:
    pull_data(d)

