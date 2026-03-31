from bs4 import BeautifulSoup
import time
import requests
import pandas as pd

url = 'https://www.worldometers.info/world-population/population-by-country/'
response = requests.get(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'})
time.sleep(2)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')

name_country = []
pop_country = []

names = soup.find('tbody').find_all('a', attrs={'data-astro-reload':'true'})
populations = soup.find('tbody').find_all('td', class_='font-bold')

for name in names:
    name_country.append(name.text)
    print(name.text)
for pop in populations[1::2]:
    pop_country.append(pop.text)
    print(pop.text)

Name_Pop = {
    'NAME': name_country,
    'POPULATION': pop_country
}

print(len(name_country), len(pop_country))
df = pd.DataFrame(Name_Pop)
df.to_excel('Название и Население стран.xlsx', index=False, engine='openpyxl')
df.to_csv('Название и Население стран.csv', index=False, encoding='utf-8-sig')