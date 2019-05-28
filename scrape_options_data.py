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
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
import os
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
from selenium.webdriver.common.keys import Keys
import time


# Create the profile to allow automatic downloads
profile = webdriver.FirefoxProfile()
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", 'application/csv');
profile.set_preference("browser.download.panel.shown", False)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/csv,attachment/csv,text/comma-separated-values")
profile.set_preference("browser.download.folderList", 2);
profile.set_preference("browser.download.dir", "~/Downloads")

# Set the delay
delay = 10 # seconds

# Start the browser
browser = webdriver.Firefox(firefox_profile=profile)

# Login into the options part of the website
browser.get("https://marketchameleon.com/Overview/AAPL/OptionChain/")

def login():
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'site-header')))
    except (TimeoutException, UnexpectedAlertPresentException) as e:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'site-header')))
        print("Loading took too much time!")

    browser.find_element_by_xpath('//*[@title="Log In"]').click()

    try:
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.LINK_TEXT, '403 - Forbidden: Access is denied.')))
    except TimeoutException:
        o = 0
        # do nothing and continue
    WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'UserName')))

    username_box = browser.find_element_by_xpath('//*[@id="UserName"]')
    password_box = browser.find_element_by_xpath('//*[@id="Password"]')

    username_box.send_keys('jared.eisenberg2@gmail.com')
    password_box.send_keys('4762651Fei#')
    password_box.send_keys(Keys.ENTER)
    WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.montage_datepicker_trigger')))

def create_dates(start, end):
    dates = []
    delta = end - start
    for i in range(delta.days + 1):
        dates.append(start + timedelta(days=i))
    return dates

def find_date(ticker, year, month, month_value, day):
    browser.get("https://marketchameleon.com/Overview/" + ticker + "/OptionChain/")
    # get the right date as entered above
    date_btn = browser.find_element_by_xpath('//a[@class="montage_datepicker_trigger"]')
    WebDriverWait(browser, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.montage_datepicker_trigger')))
    date_btn.click()

    '''
    try:
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select.ui-datepicker-year')))
    except TimeoutException:
        date_btn = browser.find_element_by_xpath('//a[@class="montage_datepicker_trigger"]')
        date_btn.click()
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select.ui-datepicker-year')))
    '''
    year_btn_holder = browser.find_element_by_xpath('//select[@class="ui-datepicker-year"]')
    year_btn = year_btn_holder.find_element_by_xpath('//option[@value="' + year + '"]')
    year_btn.click()
    WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, '//select[@class="ui-datepicker-month"]')))
    month_btn_holder = browser.find_element_by_xpath('//select[@class="ui-datepicker-month"]')
    month_btn = month_btn_holder.find_element_by_xpath('//option[text() = "' + month + '"]')
    month_btn.click()
    day_btn_holder = browser.find_element_by_xpath('//table[@class="ui-datepicker-calendar"]')
    day_btn = day_btn_holder.find_element_by_xpath('//a[text()="' + day + '"]/ancestor::td[@data-month="' + month_value + '"]')
    day_btn.click()

    WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, '//a[text()="' + day + '-' + month + '-' + year + '"]')))

if __name__ == '__main__':
    # Login into the website
    login()

    # Load in the dates and tickers
    dataframe = pd.read_csv('comps_dates_testing.csv')
    tickers = dataframe['Name'].tolist()
    dates_begin = dataframe['Date Begin'].tolist()
    dates_end = dataframe['Date End'].tolist()
    for i, val in enumerate(tickers):
        date_b = datetime.strptime(dates_begin[i], "%Y-%m-%d")
        date_e = datetime.strptime(dates_end[i], "%Y-%m-%d")
        dates = create_dates(date_b, date_e)
        print(val, dates_begin[i], dates_end[i])
        for d in dates:
            find_date(val, str(d.year), d.strftime('%b'), str(d.month - 1), str(d.day))
            browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]/div[3]/div/div[3]/div[3]/div[1]/span').click()
            time.sleep(5)
