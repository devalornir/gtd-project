import re
import bs4
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


import seaborn as sns
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

# func to create a soup obj from a html source
def load_html_to_soup(html_source):
    bsobj = soup(html_source, 'html.parser')
    return bsobj

URL = "https://www.start.umd.edu/gtd/search/Results.aspx?page=405&chart=injuries&casualties_type=&casualties_max=&count=100"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(URL)
time.sleep(10)


# Defining of the dataframe
df = pd.DataFrame(columns=['Date', 'Country', 'City', 'Perpetrator', 'Fatalities', 'Injured', 'Target'])

for i in range(100):
    try:
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "results-table"))
        )
    except:
        print("Exiting with error")
        driver.quit()

    bsobj = load_html_to_soup(driver.page_source)
    #  Looking for the table with the class 'results'
    tableobj = bsobj.find('table', class_='results')
    # Collecting Ddata
    for row in tableobj.tbody.find_all('tr'):    
    # Find all data for each column
    # columns[i].text.strip() for text
    # columns[j].span.contents[0].strip('&0.') for number
        columns = row.find_all('td')
        if(columns != []):
            incident_date = columns[1].text.strip()
            countery = columns[2].text.strip()
            city = columns[3].text.strip()
            perpetrator = columns[4].text.strip()
            fatalities = columns[5].text.strip()
            injured = columns[6].text.strip()
            target = columns[7].text.strip()
            df_new_row = pd.DataFrame({
                'Date': [incident_date],
                'Country': [countery],
                'City': [city], 
                'Perpetrator': [perpetrator], 
                'Fatalities': [fatalities], 
                'Injured': [injured], 
                'Target': [target]
            })
            df = pd.concat([df, df_new_row], ignore_index=True)
    nextResultButton = driver.find_element(by=By.PARTIAL_LINK_TEXT, value="MORE RESULTS")
    nextResultButton.click()

df.to_csv('output.csv', mode='a', header=False)
driver.quit()



# bsobj = load_soup_object(URL)






