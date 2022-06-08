#Coinmarketcap API
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
from time import sleep
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start':'1',
    'limit':'100',
    'convert':'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'bdbd3671-ade8-4563-8283-b9f0b97a4f3f',
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

def api_runner():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
     'start':'1',
     'limit':'100',
     'convert':'USD'
    }
    headers = {
     'Accepts': 'application/json',
     'X-CMC_PRO_API_KEY': 'bdbd3671-ade8-4563-8283-b9f0b97a4f3f',
    }   
    session = Session()
    session.headers.update(headers)
    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
    df = pd.json_normalize(data['data'])
    df['timestamp'] = pd.Timestamp.now()
    if not os.path.isfile(r"C:/Users/RobertBartalis/Desktop/Python/coinmarketcap/API.csv"):
      df.to_csv(r"C:/Users/RobertBartalis/Desktop/Python/coinmarketcap/API.csv", header='column_names')
    else:
        df.to_csv(r"C:/Users/RobertBartalis/Desktop/Python/coinmarketcap/API.csv", mode='a', header=False)

for i in range (5):
    api_runner()
    print('loop nr. ' + str(i) + ' completed!')
    sleep(2) 


df2 = pd.read_csv('C:/Users/RobertBartalis/Desktop/Python/coinmarketcap/API.csv')

df3 = df2.groupby('name', sort=False)['quote.USD.percent_change_1h',	'quote.USD.percent_change_24h',	'quote.USD.percent_change_7d',	'quote.USD.percent_change_30d',	'quote.USD.percent_change_60d',
	'quote.USD.percent_change_90d'].mean()

df4 = df3.stack()
df4 = df4.to_frame(name='values')
index = pd.Index(range(100))
df5 = df4.reset_index()

df5 = df5.rename(columns={'level_1':'percent_change'})

df5['percent_change'] = df5['percent_change'].replace(['quote.USD.percent_change_1h',	'quote.USD.percent_change_24h',	'quote.USD.percent_change_7d',	'quote.USD.percent_change_30d',	'quote.USD.percent_change_60d',
	'quote.USD.percent_change_90d'],['1h','24h', '7d', '30d', '60d', '90d'])

sns.catplot(x='percent_change', y='values', data=df5[0:91], kind='point', hue='name')
plt.show()
