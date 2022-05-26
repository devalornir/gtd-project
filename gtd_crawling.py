import re
import bs4
import pandas as pd
import numpy as np
from selenium import webdriver

import seaborn as sns
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

PATH = "C:\Program Files (x86)\chromdriver.exe"
driver = webdriver.chrome(PATH)

#function to create and return a soup object for a given html file.
def load_soup_object(url):
    data = requests.get(url).text
    bsobj = soup(data, 'html.parser')
    return bsobj

URL = "https://www.start.umd.edu/gtd/search/Results.aspx?chart=injuries&casualties_type=&casualties_max=&count=100"
# gtd_page = urlopen(URL)
# resp = requests.get(URL)
# print(resp.status_code)
# print(resp.text)

# resp = requests.get(URL)
# if resp.status_code == 200:
#    csvtext = resp.text
#    csvbuffer = io.StringIO(csvtext)
#    df = pd.read_csv(csvbuffer)
#    print(df)
bsobj = load_soup_object(URL)

#  Looking for the table with the class 'results'
table = bsobj.find('table', class_='results')

# Defining of the dataframe
df = pd.DataFrame(columns=['Date', 'Country', 'City', 'Perpetrator', 'Fatalities', 'Injured', 'Target'])

# Collecting Ddata
for row in table.tbody.find_all('tr'):    
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

        df = df.append(
            {
            'Date': incident_date,
            'Country': countery,
            'City': city, 
            'Perpetrator': perpetrator, 
            'Fatalities': fatalities, 
            'Injured': injured, 
            'Target': target
            }, ignore_index=True)

print(df)



