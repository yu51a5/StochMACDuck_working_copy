# import yfinance as yf
# see https://pypi.org/project/yfinance/
# URL API 
# https://stackoverflow.com/questions/44030983/yahoo-finance-url-not-working
# https://stackoverflow.com/questions/76632893/exists-and-getsymbols-cant-find-symbol-listed-in-yahoo
# https://stackoverflow.com/questions/76065035/yahoo-finance-v7-api-now-requiring-cookies-python
# https://www.datapears.com/post/connect-to-yahoo-finance-building-a-stock-market-tracker

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
data_types = {k : ({'Date' : np.datetime64}) for k in ["div", "history", "split"]}

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
             "events" : "history", # "history%7div%7Csplit", #
             "includeAdjustedClose" : "true"}
  
  result_dict = {}
  
  for eve, dt in data_types.items():
    params["events"] = eve
    response = requests_get(url=apiBase1 + '/v7/finance/download/' + symbol, params=params)
    if response.status_code == 200:
      # print(response.text)
      result_dict[eve] = pd.read_csv(io.StringIO(response.text), index_col='Date')
      result_dict[eve].index = pd.to_datetime(result_dict[eve].index, format='%Y-%m-%d')

  return result_dict

get_symbol_history(symbol='AAPL', first_date=datetime.date(2023, 9, 14), last_date=datetime.date(2023, 12, 13), interval="1d")
get_symbol_history(symbol='AAPL', first_date=datetime.date(2022, 12, 13), last_date=datetime.date(2023, 12, 13), interval="1mo")

def _stock_query(stock_ticker, first_date, last_date):
  # Download the historical data for the asset
  #stock = yf.Ticker(stock_ticker)

  stock_info = get_symbol_quote(symbols=[stock_ticker])[0]

  info = {key : stock_info.get(key, None) for key in ('longName', 'exchange', 'quoteType', 'currency', 'marketState')}

  print(stock_ticker, info)
  
  result_dict = get_symbol_history(symbol=stock_ticker, first_date=first_date, last_date=last_date) #stock.history(start=first_date, end=last_date)
  #dates = [d.date() for d in data.axes[0].to_pydatetime().tolist()]

  result_dict["history"].rename({s : s.lower() for s in ['Open', 'High', 'Low', 'Close', 'Volume']}, axis=1, inplace=True)
  #result.index = result.index.tz_localize(tz=None)
  #history_indicators[ticker].index = history_indicators[ticker].index.tz_localize(None)
  # https://stackoverflow.com/questions/61104362/how-to-get-actual-stock-prices-with-yfinance
  current_prices = [stock_info.get('regularMarketPrice', None), stock_info.get('currentPrice', None), result_dict["history"]['close'].iloc[-1]]
  if (current_prices[0] is not None) or (current_prices[1] is not None):
    if (current_prices[0] is not None):
      if (current_prices[1] is not None):
        assert 1, ()
      current_price = current_prices[0]
    else:
      current_price = current_prices[1]
    extrapolate = True
  else:
    current_price = result['close'].iloc[-1]
    
    extrapolate = max([abs( result_dict["history"][label].iloc[-1]) for label in ["open", "high", "low"]]) < 1E-8
    
  
  print(current_price)
  #print(result.tail(1))
  #print('current prices for', stock_ticker, current_price, result['close'].iloc[-1], (current_price / result['close'].iloc[-1] - 1))
  #print(result.iloc[-1])
  
  info['extrapolated'] = extrapolate

  
  extrapolated_minus_one = False
  index_minus_one = result_dict["history"].index[-1]
  index_minus_two = result_dict["history"].index[-2]
  if (result_dict["history"].at[index_minus_one, 'open'] > 1E-8) and (result_dict["history"].at[index_minus_one, 'close'] < 1E-8):
    pass
  elif result_dict["history"].at[index_minus_one, 'close'] < 1E-8:
     DataFrame.drop(index=index_minus_one)
  else:
    for label in ["open", "high", "low"]:
      if result_dict["history"].at[index_minus_one, label] < 1E-8:
        result_dict["history"].at[index_minus_one, label] = result_dict["history"].at[index_minus_two, 'close' if label == 'open' else label]
        extrapolated_minus_one = True
  
  return info, result_dict

  