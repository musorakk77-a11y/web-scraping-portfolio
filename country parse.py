from bs4 import BeautifulSoup
import time
import requests
import pandas as pd

try:
    url = 'https://www.scrapethissite.com/pages/simple/'
    response = requests.get(url, timeout=5, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'})
    time.sleep(3)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    name_country = []
    population_country = []

    names = soup.select('h3.country-name')
    populations = soup.select('span.country-population')

    for name in names:
        name_country.append(name.text.strip())

    for pop in populations:
        population_country.append(pop.text.strip())
    
    data = {
        'Name country': name_country,
        'Population country' : population_country
    }

    df = pd.DataFrame(data)
    df.to_excel('names&population cotry.xlsx', index=False, engine='openpyxl')
    df.to_csv('names&population cotry.csv', index=False, encoding='utf-8-sig')
except requests.exceptions.ConnectionError:
    print('нет интернета')
except requests.exceptions.Timeout:
    print('сайт не ответил')
except AttributeError:
    pass
