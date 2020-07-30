import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from time import sleep
from random import randint

URL = 'https://www.bazar.kg/kyrgyzstan/elektronika/telefony-gadzhety?'


#initialize empty lists where you'll store your data

titles = []
prices = []
links = []


#pagination
pages = np.arange(1,67+1)
page_count = 0

for page in pages:
    page = requests.get(URL+str(page))
    soup = BeautifulSoup(page.text, 'html.parser')
    soup.find_all('div', class_='listing')
    gadzhety_div = soup.find_all('div', class_='listing')

    sleep(randint(2,5))
    page_count += 1

    print('Page ', page_count, ' parsed.')


    #initiate the 'for' loop 
    #this tells your scraper to iterate through 
    #every div container we stored in gadzhety_div
    for container in gadzhety_div:
    
    #name
        name = container.find('p', class_='title').get_text(strip=True)
        titles.append(name)
    
    #price
        price = container.find('p', class_='price').get_text(strip=True)
        prices.append(price)
    
    #link
        link = container.find('a').get('href')
        links.append('https://www.bazar.kg' + link)


#building our Pandas dataframe
gadzhety = pd.DataFrame({
        'titles': titles,
        'prices': prices,
        'links': links,
})

#cleaning data with Pandas
# gadzhety['prices'] = gadzhety['prices'].str.extract('(\d+)').astype(int)

print(len(titles), ' gadgets received.')
gadzhety.to_csv('bazar.kg_gadzhety.csv')