import requests
import os
import json
import difflib 
from bs4 import BeautifulSoup
import pandas as pd

from pyti.smoothed_moving_average import smoothed_moving_average as sma
from pyti.bollinger_bands import lower_bollinger_band as lbb

API_KEY = 'I15410OY48G62FRG'

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}'

companies = json.load(open('./companies-symbols/companies.json'))

def snp500():
    c = requests.get('https://www.slickcharts.com/sp500').content
    page = BeautifulSoup(c, 'html.parser')
    page.prettify()

    table = page.findAll('tr')[1:]

    contained_data = open('./companies-symbols/companies.json', 'w+')
    contained_data.write('{\n')

    for i in table:
        company = i.find_all('td')[1].text
        symbol = i.find_all('td')[2].text
        if i == table[-1]:
            contained_data.write(f"\"{company.lower()}\": \"{symbol}\"\n")
        else:
            contained_data.write(f"\"{company.lower()}\": \"{symbol}\",\n")

    contained_data.write('}\n')
    contained_data.close()

def createFolder(path_insert=False):
    directory = './data/'
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

def check_path(stock_name):
    stock_path = f'./data/{stock_name}.csv'

    if os.path.exists(stock_path):
        pass
    elif not os.path.exists('./data/'):
        createFolder()
    
    return stock_path

def add_stock_details(stock_name):
    response = requests.get(url.format(stock_name, API_KEY))

    if response.status_code == 200 and 'Error Message' not in response.json().keys():
        # Creating finding path or creating path 
        stock_path = check_path(stock_name)

        dictionary = response.json()['Time Series (Daily)']

        exit()

        try:
            # df = pd.DataFrame(
            #     [i, j['1. open'], j['2. high'], j['3. low'], j['4. close'], j['5. volume'], sma(list(j['4. close']), 10), sma(list(j['4. close']), 30), lbb(list(j['4. close']), 14)] for i, j in dictionary.items()
            # )
            sma = []
            fma = []
            for i in range(len(dictionary)):
                if i % 10 == 0:
                    # sma.append(dictionary[i].
                    pass

        # col_names = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Fast SMA', 'Slow SMA', 'Low BOLL']

        # df.columns = col_names
        # for col in col_names:
        #     try:
        #         df[col] = df[col].astype(float)
        #     except:
        #         df[col] = df[col].astype(str)

        # df.to_csv(stock_path, encoding='utf-8', index=False)

    elif response.status_code == 400:
        print('Failed')
    else: 
        print(f'Error finding {stock_name}, have you type it in correctly')

def find_request():
    while True:
        try: 
            string = str(input('Search for a business: ')).lower()
        except:
            print('Sorry, I did not get that')
        else:
            pass

        value = difflib.get_close_matches(string, companies.keys())

        if value:
            newValueAnswer = str(input(f'Did you mean {value[0]}? yes(y) or no(n): ')).lower()
            value = value[0]

            if newValueAnswer[0] == 'y' and value:
                if value in companies:
                    return companies[value]
                    break
        
        print('Sorry the word does not exist please double check')

if __name__ == "__main__":

    company_SYMB = find_request()

    add_stock_details(company_SYMB)
