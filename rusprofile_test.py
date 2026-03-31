from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

driver = webdriver.Chrome()
driver.get('https://www.rusprofile.ru/codes/850000')
wait = WebDriverWait(driver, 10)

data = {
    'Link org': [],
    'Name org': [],
    'CEO': [],
    'Adress org':[],
    'INN': [],
    'OGRN':[],
    'Reg data':[]
}

org_list_elem = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'list-element')))

for list_elem in org_list_elem:
    try:
        link_name_org = list_elem.find_element(By.CLASS_NAME, 'list-element__title')
        data['Link org'].append(link_name_org.get_attribute("href"))
        data['Name org'].append(link_name_org.text)
        first_spans = list_elem.find_elements(By.CLASS_NAME, 'list-element__text')
        seo = first_spans[1].text if len(first_spans) > 1 else 'не указано'
        data['CEO'].append(seo)
        data['Adress org'].append(list_elem.find_element(By.CLASS_NAME, 'list-element__address').text)
        second_spans = list_elem.find_elements(By.CSS_SELECTOR, 'div.list-element__row-info span')
        inn = second_spans[0].text.replace('ИНН: ', '').strip() if len(second_spans) > 0 else 'не указано'
        ogrn = second_spans[1].text.replace('ОГРН: ', '').strip() if len(second_spans) > 1 else 'не указано'
        reg_data = second_spans[2].text.replace('Дата регистрации: ', '').strip() if len(second_spans) > 2 else 'не указано'
        data['INN'].append(inn)
        data['OGRN'].append(ogrn)
        data['Reg data'].append(reg_data)
    except Exception as e:
        print(f'Пропущен элемент: {e}')
        continue  

driver.quit()

df = pd.DataFrame(data)
df.to_excel('Образование(код - 85).xlsx', index = False, engine = 'openpyxl')
df.to_csv('Образование(код - 85).csv', index = False, encoding = 'utf-8-sig')