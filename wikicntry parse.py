from bs4 import BeautifulSoup
import time
import requests
import pandas as pd

try:
    
    url = 'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population_(United_Nations)'
    response = requests.get(url, timeout=5, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'})
    time.sleep(3)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    
    name_cntry = []
    popul_cntry = []
    reg_cntry = []

    data_st = soup.find('tbody').find_all('tr', class_ = None)
    for data_st1 in data_st:
        data_st2 = data_st1.find_all('td')
        if len(data_st2) > 3:
            name_cntry.append(data_st2[0].text.strip())
            popul_cntry.append(data_st2[2].text.strip())
            reg_cntry.append(data_st2[4].text.strip())

    data = {
        'NAME COUNTRY': name_cntry,
        'POPULATION COUNTRY': popul_cntry,
        'REGION COUNTRY': reg_cntry
    }

    df = pd.DataFrame(data)
    df.to_excel('info country.xlsx', index=False, engine='openpyxl')
    df.to_csv('info country.csv', index=False, encoding='utf-8-sig')

except requests.exceptions.ConnectionError:
    print('нет интернета')

except requests.exceptions.Timeout:
    print('сайт не ответил')

except AttributeError:
    pass