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
from selenium.webdriver import ActionChains
import pandas as pd
import os
import time

#URL to be scraped
url_trend = 'https://www.investing.com/equities/trending-stocks'

def tooltip_extract_popularity(soup):
    soup_tool = soup.find('div',{'class':'highcharts-tooltip'})
    tool_data = soup_tool.find('div').text
    return tool_data
def tooltip_extract_sector(soup):
    soup_tool = soup.find('div',{'class':'highcharts-tooltip'})
    tool_data = soup_tool.find('div').text
    return tool_data

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

#Session
driver = webdriver.Chrome(ChromeDriverManager().install())
#driver = webdriver.Chrome()
driver.implicitly_wait(5)
driver.get(url_trend)

# Question 2 Function for hovering over bar in Popularity chart and return its data
def tooltip_popularity():
    check_and_close_signup()
    tooltip_element = driver.find_elements_by_xpath("//*[name()='div' and @id='trendingByPopularityChart']//*[name()='svg']//*[name()='g' and @class='highcharts-series highcharts-tracker'] /*[name()='rect']")
    for matches in tooltip_element:
        hover = ActionChains(driver).move_to_element(matches)
        hover.perform()
        try:
            tooltip_content_element = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.highcharts-tooltip")))
        except TimeoutException as e:
            print(e)
            return None
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        souped_data = tooltip_extract_popularity(soup)
        soup_print = print(souped_data)
    return soup_print
# Question 3 Function for hovering over bar in Sector chart and return its data
def tooltip_sector():
    check_and_close_signup()
    tooltip_element = driver.find_elements_by_xpath("//*[name()='div' and @id='trendingBySectorChart']//*[name()='svg']//*[name()='g' and @class='highcharts-series highcharts-tracker'] /*[name()='rect']")
    for matches in tooltip_element:
        hover = ActionChains(driver).move_to_element(matches)
        hover.perform()
        try:
            tooltip_content_element = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.highcharts-tooltip")))
        except TimeoutException as e:
            print(e)
            return None
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        souped_data = tooltip_extract_sector(soup)
        soup_print = print(souped_data)
    return soup_print

tooltip_data_popularity = tooltip_popularity()
print(tooltip_data_popularity)
#tooltip_data_sector = tooltip_sector()
#print(tooltip_data_sector)




driver.close()

