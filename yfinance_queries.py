import yfinance as yf
# see https://pypi.org/project/yfinance/

def _stock_query(stock_ticker, first_date, last_date):
  # Download the historical data for the asset
  stock = yf.Ticker(stock_ticker)
  result = stock.history(start=first_date, end=last_date)
  #dates = [d.date() for d in data.axes[0].to_pydatetime().tolist()]
  
  result.rename({s : s.lower() for s in ['Open', 'High', 'Low', 'Close', 'Volume']}, axis=1, inplace=True)
  index = result.index
  index = index.tz_localize(tz=None)
  result.index = index
  #history_indicators[ticker].index = history_indicators[ticker].index.tz_localize(None)
  result['Data Date'] = result.index.strftime('%Y-%m-%d')
  # https://stackoverflow.com/questions/61104362/how-to-get-actual-stock-prices-with-yfinance
  # current_price = stock.info.get('regularMarketPrice', stock.info.get('currentPrice', result['close'].iloc[-1]))
  #print(result.tail(1))
  #print('current prices for', stock_ticker, current_price, result['close'].iloc[-1], (current_price / result['close'].iloc[-1] - 1))
  if max([abs( result[label].iloc[-1]) for label in ["open", "high", "low"]]) < 1E-8:
    result['open'].iloc[-1] = result['close'].iloc[-2]
    result['low' ].iloc[-1] = result['low'  ].iloc[-2]
    result['high'].iloc[-1] = result['high' ].iloc[-2]
    #result.drop(result.tail(1).index,inplace=True)
    #print('DROPS')
  
  return result

def get_longname(stock_ticker):
  ticker_obj = yf.Ticker(stock_ticker)
  # if ticker_obj.info fails, run the following line in Shell
  # pip install --upgrade yfinance 
  company_name = ticker_obj.info['longName']
  return company_name
  