import yfinance as yf
# see https://pypi.org/project/yfinance/

def _stock_query(stock_ticker, first_date, last_date):
  # Download the historical data for the asset
  stock = yf.Ticker(stock_ticker)

  info = {key : stock.info.get(key, None) for key in ('longName', 'country', 'exchange', 'quoteType', 'currency', 'marketState')}
  
  result = stock.history(start=first_date, end=last_date)
  #dates = [d.date() for d in data.axes[0].to_pydatetime().tolist()]
  
  result.rename({s : s.lower() for s in ['Open', 'High', 'Low', 'Close', 'Volume']}, axis=1, inplace=True)
  index = result.index
  index = index.tz_localize(tz=None)
  result.index = index
  #history_indicators[ticker].index = history_indicators[ticker].index.tz_localize(None)
  result['Data Date'] = result.index.strftime('%Y-%m-%d')
  # https://stackoverflow.com/questions/61104362/how-to-get-actual-stock-prices-with-yfinance
  current_prices = [stock.info.get('regularMarketPrice', None), stock.info.get('currentPrice', None), result['close'].iloc[-1]]
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
  if result.at[index_minus_one, 'close'] < 1E-8:
     DataFrame.drop(index=index_minus_one)
  else:
    for label in ["open", "high", "low"]:
      if result.at[index_minus_one, label] < 1E-8:
        result.at[index_minus_one, label] = result.at[index_minus_two, 'close' if label == 'open' else label]
        extrapolated_minus_one = True
  
  return info, result

  