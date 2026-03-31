from bs4 import BeautifulSoup
import time
import requests
import pandas as pd

try:
    url = 'https://www.scrapethissite.com/pages/forms/'
    response = requests.get(url, timeout=5, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'})
    time.sleep(3)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    name_team = []
    year_team = []
    wins_team = []
    losses_team = []

    while soup.find('a', attrs={'aria-label':'Next'}):
        try:
            names = soup.find_all('td', class_='name')
            years = soup.find_all('td', class_ = 'year')
            wins = soup.find_all('td', class_='wins')
            losses = soup.find_all('td', class_='losses')

            for name in names:
                name_team.append(name.text.strip())
            for year in years:
                year_team.append(year.text.strip())
            for win in wins:
                wins_team.append(win.text.strip())
            for lose in losses:
                losses_team.append(lose.text.strip())
            
            nxt_but = soup.find('a', attrs={'aria-label':'Next'})['href']
            cur_url = 'https://www.scrapethissite.com/' + nxt_but
            response = requests.get(cur_url, timeout=5)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml')        
        
        except requests.exceptions.ConnectionError:
            print('нет интернета')        
        except requests.exceptions.Timeout:
            print('сайт не ответил')        
        except AttributeError:
            break

    for name in names:
        name_team.append(name.text.strip())    
    for year in years:
        year_team.append(year.text.strip())    
    for win in wins:
        wins_team.append(win.text.strip())    
    for lose in losses:
        losses_team.append(lose.text.strip()) 

    data = {
        'NAME TEAM': name_team,
        'YEAR': year_team,
        'WINS': wins_team,
        'LOSSES': losses_team
    }          
    
    df = pd.DataFrame(data)
    df.to_excel('hockey info.xlsx', index=False, engine='openpyxl')
    df.to_csv('hockey info.csv', index=False, encoding='utf-8-sig')
except requests.exceptions.ConnectionError:
    print('нет интернета')
except requests.exceptions.Timeout:
    print('сайт не ответил')
except AttributeError:
    pass
