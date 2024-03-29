# import yfinance as yf
# see https://pypi.org/project/yfinance/
# URL API 
# https://stackoverflow.com/questions/44030983/yahoo-finance-url-not-working
# https://stackoverflow.com/questions/76632893/exists-and-getsymbols-cant-find-symbol-listed-in-yahoo
# https://stackoverflow.com/questions/76065035/yahoo-finance-v7-api-now-requiring-cookies-python
# https://www.datapears.com/post/connect-to-yahoo-finance-building-a-stock-market-tracker

# https://medium.com/geekculture/the-best-free-stock-market-data-apis-available-in-2021-1ecfa51ee619
# https://www.xignite.com/news/best-6-free-and-paid-stock-market-apis/
# https://rapidapi.com/blog/best-stock-api/
# https://finnhub.io

import requests
import datetime
import time
import pandas as pd
import numpy as np
import io

apiBase1= 'https://query1.finance.yahoo.com'
apiBase = 'https://query2.finance.yahoo.com'
headers = { 
  "User-Agent": 
  "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
}

credentials = None
# {v : np.float64 for v in (['Open', 'High', 'Low', 'Close', 'Volume'] if k == "history" else ["Dividends" if k == "div" else 'Stock Splits'])}.update
data_names = {"div" : 'Dividends', "split" : 'Splits', "history" : "history"}

#"https://query1.finance.yahoo.com/v7/finance/chart/AAPL?period1=1694649600&period2=1702425600&interval=1d&indicators=RSI&includeTimestamps=true"
#https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1694649600&period2=1702425600&interval=1d&events=div&includeAdjustedClose=true
#https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1694649600&period2=1702425600&interval=1d&events=div&includeAdjustedClose=true&crumb=auA1R4VT1hs

def requests_get(url, params={}, cookieUrl='https://fc.yahoo.com', crumbUrl=apiBase+'/v1/test/getcrumb'):
  global credentials 
  if credentials is None:
    print(f'{datetime.datetime.now()}: started getting yahoo finance credentials. This might take ca. 20 seconds.')
    cookie = requests.get(cookieUrl).cookies
    crumb = requests.get(url=crumbUrl, cookies=cookie, headers=headers).text
    print(f'{datetime.datetime.now()}: completed getting yahoo finance credentials')
    credentials = {'cookie': cookie, 'crumb': crumb}
  params['crumb'] = credentials['crumb']
  response = requests.get(url, params=params, cookies=credentials['cookie'], headers=headers)
  return response

def get_symbol_quote(symbols):
  response = requests_get(url=apiBase + '/v7/finance/quote', params={'symbols': ','.join(symbols)})
  quotes = response.json()['quoteResponse']['result']
  return quotes

def get_symbol_history(symbol, first_date, last_date, interval="1d"):
  params = { "period1" : int(time.mktime(first_date.timetuple())),
             "period2" : int(time.mktime( last_date.timetuple())),
             "interval" : interval,
             "events" : None,
             "includeAdjustedClose" : "true"}
  
  result_dict = {}
  
  for eve, dn in data_names.items():
    params["events"] = eve
    response = requests_get(url=apiBase1 + '/v7/finance/download/' + symbol, params=params)
    if response.status_code == 200:
      # print(response.text)
      result_dict[dn] = pd.read_csv(io.StringIO(response.text), index_col='Date')
      result_dict[dn].index = pd.to_datetime(result_dict[dn].index, format='%Y-%m-%d')

  return result_dict

def stock_query(stock_ticker, first_date, last_date):

  stock_info = get_symbol_quote(symbols=[stock_ticker])

  if not stock_info:
    return None, None, None, None
    
  stock_info = stock_info[0]
  info = {key : stock_info.get(key, None) for key in ('longName', 'exchange', 'quoteType', 'currency', 'marketState')}
  
  result_dict = get_symbol_history(symbol=stock_ticker, first_date=first_date, last_date=last_date) 

  result_dict["history"].rename({s : s.lower() for s in ['Open', 'High', 'Low', 'Close', 'Volume']}, axis=1, inplace=True)
  #result.index = result.index.tz_localize(tz=None)
  #history_indicators[ticker].index = history_indicators[ticker].index.tz_localize(None)
  # https://stackoverflow.com/questions/61104362/how-to-get-actual-stock-prices-with-yfinance

  df = result_dict["history"]
  while len(df.index):
    for label in ['close', 'open']:
      current_price = df[label].iloc[-1]
      if current_price is not None:
        break
    df = df.drop(index=df.index[-1])
    
  current_prices = [stock_info.get('regularMarketPrice', None), stock_info.get('currentPrice', None)]
  if (current_prices[0] is not None) or (current_prices[1] is not None):
    if (current_prices[0] is not None):
      if (current_prices[1] is not None):
        assert abs(current_prices[0] - current_prices[1]) < 1E-8, "current prices are not equal"
      current_price = current_prices[0]
    else:
      current_price = current_prices[1]
  
  info['current_price'] = current_price
  
  return info, result_dict["history"], result_dict['Dividends'], result_dict['Splits']

  