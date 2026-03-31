from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

url = 'https://books.toscrape.com/'
response = requests.get(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'})
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')
time.sleep(2)

name_book = []
price_book = []

while soup.find('li', class_ = 'next'):
    try:
        names = soup.find_all('h3')
        prices = soup.find_all('p', class_ = 'price_color')
        
        for name in names:
            name_book.append(name.find('a')['title'])
        
        for price in prices:
            price_book.append(price.get_text())
          
        btn_next = soup.find('li', class_ = 'next').find('a')['href']
        if btn_next.startswith('catalogue'):
            current_url = 'https://books.toscrape.com/' + btn_next
        else:
            current_url = 'https://books.toscrape.com/catalogue/' + btn_next
        response = requests.get(current_url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')  
    except AttributeError:
        break

for name in soup.find_all('h3'):
    name_book.append(name.find('a')['title'])
for price in soup.find_all('p', class_ = 'price_color'):
    price_book.append(price.get_text())
price_book = [p.strip()[1:] for p in price_book]
name_price = {
            'Name Book': name_book,
            'Price Book': price_book
        }
df = pd.DataFrame(name_price)
df.to_excel('Название_и_цена_книги.xlsx', index=False, engine='openpyxl')
df.to_csv('Название_и_цена_книги.csv', index=False, encoding='utf-8-sig')