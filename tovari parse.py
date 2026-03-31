from bs4 import BeautifulSoup
import time
import requests
import pandas as pd

try:
    url = 'https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops'
    response = requests.get(url, timeout=5, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'})
    time.sleep(3)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    data = {
        'NAME': [],
        'PRICE': [],
        'RATING': []
    }

    names = soup.find_all('a', class_='title')
    prices = soup.find_all('span', attrs={'itemprop':'price'})
    ratings = soup.find_all('p',attrs={'data-rating': True})

    for name in names:
        data['NAME'].append(name['title'])
    for price in prices:
        data['PRICE'].append(price.text.replace('$', ''))
    for rating in ratings:
        data['RATING'].append(rating['data-rating'])
    
    df = pd.DataFrame(data)
    df.to_excel('.xlsx', index=False, engine='openpyxl')
    df.to_csv('.csv', index=False, encoding='utf-8-sig')
except requests.exceptions.ConnectionError:
    print('нет интернета')
except requests.exceptions.Timeout:
    print('сайт не ответил')
except AttributeError:
    pass