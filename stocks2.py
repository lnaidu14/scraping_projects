import bs4
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import os




#URL to be scraped
url_trend = 'https://www.investing.com/equities/trending-stocks'

def table_within_trendingInnerContent_div_to_pandas(soup):
    
    table_div = soup.find('div' , {'id': 'trendingInnerContent'})
    table = table_div.find('table')
    df = pd.read_html(str(table))
    return df

def check_and_close_signup():
    try:
        signup_element = driver.find_element_by_css_selector('div.signupWrap.js-gen-popup.dark_graph')
        if signup_element.is_displayed():
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            return None
        else:
            return None
    except (TimeoutException, NoSuchElementException) as e:
        pass
    finally:
        pass

def get_table_by_filter_id_to_pandas(filter_name):
    check_and_close_signup()
    filter_button = driver.find_element_by_id(filter_name)
    filter_button.click()
    try:
        trendingInnerContent_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table.genTbl.closedTbl.elpTbl.crossRatesTbl")))
    except TimeoutException as e:
        print(e)
        return None
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table_df = table_within_trendingInnerContent_div_to_pandas(soup)
    return table_df

def stockSoup(url):    
    r = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
    data = bs4.BeautifulSoup(r.text,'html.parser')
    return data
     
soup = stockSoup(url_trend)

#Question 1 Scraping the Trending Stocks
for stock_Values in soup.find_all('div',{'id': 'microChartData' }):
    name = stock_Values.find('a').text
    value = stock_Values.find('div').text
    print(name,value)
    
#2 Question 4 for scraping Trending Stock Quotes by setting up a session and clicking the links to retrieve JS source finally the data stored in them
#Session setup
driver = webdriver.Chrome(ChromeDriverManager().install())
#driver = webdriver.Chrome()
driver.implicitly_wait(5)
driver.get(url_trend)
#4
filter_price_df = get_table_by_filter_id_to_pandas('filter_price')
filter_performance_df = get_table_by_filter_id_to_pandas('filter_performance')
filter_technical_df = get_table_by_filter_id_to_pandas('filter_technical')
filter_fundamental_df = get_table_by_filter_id_to_pandas('filter_fundamental') 

if filter_price_df:
    print(filter_price_df[0].to_string)
if filter_performance_df:
    print(filter_performance_df[0].to_string)
if filter_technical_df:
    print(filter_technical_df[0].to_string)
if filter_fundamental_df:
    print(filter_fundamental_df[0].to_string)

driver.close()



