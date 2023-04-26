import yfinance as yf
import pandas as pd
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
  if max([abs( result[label].iloc[-1]) for label in ["open", "high", "low"]]) < 1E-8:
    result.drop(result.tail(1).index,inplace=True)
  
  return result
  