from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

driver = webdriver.Chrome()
driver.get('https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops')

# Ждём пока появится хотя бы один элемент с классом 'title'
# EC — это набор условий: element появился, кликабелен, виден и т.д.
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'title')))
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[itemprop="price"]')))
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p[data-rating]')))

titles = driver.find_elements(By.CLASS_NAME, 'title')
prices = driver.find_elements(By.CSS_SELECTOR, 'span[itemprop="price"]')
ratings = driver.find_elements(By.CSS_SELECTOR, 'p[data-rating]')

data = {
    'NAME': [],
    'PRICE': [],
    'RATE': []
}

for title in titles:
    data['NAME'].append(title.get_attribute('title'))
for price in prices:
    data['PRICE'].append(price.text.replace('$', '').strip())
for rate in ratings:
    data['RATE'].append(rate.get_attribute('data-rating'))
driver.quit()

#Выгружаю все в эксель после закрытия браузера, чтобы он не работал на фоне и не занимал оперативку(моя попытка опитимизировать программу)
df = pd.DataFrame(data)
df.to_csv('Tovari_selenium.csv', index=False, encoding='utf-8-sig')
df.to_excel('Tovari_selenium.xlsx', index=False, engine='openpyxl')
