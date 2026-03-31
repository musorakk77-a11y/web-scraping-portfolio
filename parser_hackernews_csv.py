from bs4 import BeautifulSoup
import time
import requests
import pandas as pd

url = 'https://www.chitai-gorod.ru/catalog/books/manga-110064'
headers = {'User-Agent': 'Mozilla/5.0'}

name_book = []
author_book = []
price_book = []
link_book = []

while True:
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Находим все элементы
    names = soup.find_all('a', class_='product-card__title')
    authors = soup.find_all('span', class_='product-card__subtitle')
    prices = soup.select('[class*="product-mini-card-price__price"]')
    links = soup.find_all('a', class_='product-card__title')
    
    # Просто добавляем данные, не связывая их номерами
    for name in names:
        name_book.append(name.text.strip())
    
    for author in authors:
        author_book.append(author.text.strip())
    
    for price in prices:
        price_book.append(price.text.strip())
    
    for link in links:
        full_link = 'https://www.chitai-gorod.ru' + link['href']
        link_book.append(full_link)
    
    # Ищем кнопку "дальше"
    next_btn = soup.find('a', attrs={'tabindex': '0'})
    if next_btn is None:
        break  # кнопки нет — выходим
    
    url = 'https://www.chitai-gorod.ru' + next_btn['href']
    time.sleep(2)

# Сохраняем в Excel
df = pd.DataFrame({
    'NAME': name_book,
    'AUTHOR': author_book,
    'PRICE': price_book,
    'LINK': link_book
})

df.to_excel('books.xlsx', index=False)
print(f"Готово! Собрано {len(name_book)} книг")