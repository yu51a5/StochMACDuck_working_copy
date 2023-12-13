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

apiBase1= 'https://query1.finance.yahoo.com'
apiBase = 'https://query2.finance.yahoo.com'
headers = { 
  "User-Agent": 
  "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
}

credentials = None

def getCredentials(cookieUrl='https://fc.yahoo.com', crumbUrl=apiBase+'/v1/test/getcrumb'):
  print(f'{datetime.datetime.now()}: started getting yahoo finance credentials. This might take ca. 20 seconds.')
  cookie = requests.get(cookieUrl).cookies
  crumb = requests.get(url=crumbUrl, cookies=cookie, headers=headers).text
  print(f'{datetime.datetime.now()}: completed getting yahoo finance credentials')
  return {'cookie': cookie, 'crumb': crumb}

def get_symbol_quote(symbols):
  global credentials 
  if credentials is None:
    credentials = getCredentials()
  url = apiBase + '/v7/finance/quote'
  params = {'symbols': ','.join(symbols), 'crumb': credentials['crumb']}
  response = requests.get(url, params=params, cookies=credentials['cookie'], headers=headers)
  quotes = response.json()['quoteResponse']['result']
  return quotes

def get_symbol_history(symbol, first_date, last_date):
  global credentials 
  if credentials is None:
    credentials = getCredentials()
  url = apiBase1 + '/v7/finance/download/' + symbol

  params = { "period1" : int(time.mktime(first_date.timetuple())),
             "period2" : int(time.mktime( last_date.timetuple())),
             "interval" : '1d',
             "events" : "history",
             "includeAdjustedClose" : "true",
             'crumb': credentials['crumb'] }
  response = requests.get(url, params=params, cookies=credentials['cookie'], headers=headers)
  s, u = response.status_code, response.url
  print(dir(response))
  s1 = response.json()
  s2 = response.json()['quoteResponse']
  quotes = response.json()['quoteResponse']['result']
  return quotes

get_symbol_history(symbol='AAPL', first_date=datetime.date(2023, 9, 13), last_date=datetime.date(2023, 12, 13))

def _stock_query(stock_ticker, first_date, last_date):
  # Download the historical data for the asset
  #stock = yf.Ticker(stock_ticker)

  stock_info = get_symbol_quote(symbols=[stock_ticker])[0]

  info = {key : stock_info.get(key, None) for key in ('longName', 'region', 'exchange', 'quoteType', 'currency', 'marketState')}

  print(stock_ticker, info)
  
  result = get_symbol_history(symbol=stock_ticker, first_date=first_date, last_date=last_date) #stock.history(start=first_date, end=last_date)
  #dates = [d.date() for d in data.axes[0].to_pydatetime().tolist()]
  
  result.rename({s : s.lower() for s in ['Open', 'High', 'Low', 'Close', 'Volume']}, axis=1, inplace=True)
  result.index = result.index.tz_localize(tz=None)
  #history_indicators[ticker].index = history_indicators[ticker].index.tz_localize(None)
  result['Data Date'] = result.index.strftime('%Y-%m-%d')
  # https://stackoverflow.com/questions/61104362/how-to-get-actual-stock-prices-with-yfinance
  current_prices = [stock_info.get('regularMarketPrice', None), stock_info.get('currentPrice', None), result['close'].iloc[-1]]
  if (current_prices[0] is not None) or (current_prices[1] is not None):
    if (current_prices[0] is not None):
      if (current_prices[1] is not None):
        assert ()
      current_price = current_prices[0]
    else:
      current_price = current_prices[1]
    extrapolate = True
  else:
    current_price = result['close'].iloc[-1]
    
    extrapolate = max([abs( result[label].iloc[-1]) for label in ["open", "high", "low"]]) < 1E-8
    
  
  print(current_price)
  #print(result.tail(1))
  #print('current prices for', stock_ticker, current_price, result['close'].iloc[-1], (current_price / result['close'].iloc[-1] - 1))
  #print(result.iloc[-1])
  
  info['extrapolated'] = extrapolate

  
  extrapolated_minus_one = False
  index_minus_one = result.index[-1]
  index_minus_two = result.index[-2]
  if (result.at[index_minus_one, 'open'] > 1E-8) and (result.at[index_minus_one, 'close'] < 1E-8):
    pass
  elif result.at[index_minus_one, 'close'] < 1E-8:
     DataFrame.drop(index=index_minus_one)
  else:
    for label in ["open", "high", "low"]:
      if result.at[index_minus_one, label] < 1E-8:
        result.at[index_minus_one, label] = result.at[index_minus_two, 'close' if label == 'open' else label]
        extrapolated_minus_one = True
  
  return info, result

  