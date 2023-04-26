from yfinance_queries import _stock_query as yfinance_stock_query
from datetime import timedelta


# https://medium.com/geekculture/the-best-free-stock-market-data-apis-available-in-2021-1ecfa51ee619
# https://www.xignite.com/news/best-6-free-and-paid-stock-market-apis/
# https://rapidapi.com/blog/best-stock-api/
# https://finnhub.io

stock_query_to_use = yfinance_stock_query # polygon_stock_query

def stock_query(stock_ticker, last_date, how_many_calendar_days_of_data_to_fetch):
  first_date = last_date - timedelta(days=how_many_calendar_days_of_data_to_fetch)
  
  result = stock_query_to_use(stock_ticker=stock_ticker, 
                                              first_date=first_date,
                                              last_date=last_date)
  return result
