import urllib.request, os
from ast import literal_eval
# literal_eval explainer: https://www.aipython.in/python-literal_eval/
from datetime import date, timedelta, datetime

def _run_polygon_query_and_process_results(polygon_url, print_results=True):
  polygon_url_plus = "https://api.polygon.io/" + polygon_url + "apiKey=" + os.environ[
    'apiKey']
  try:
    response = urllib.request.urlopen(polygon_url_plus)
  except Exception as ex:
    print('The exception is', ex)
    print('The query was', polygon_url_plus)
    raise ex
  if response is None:
    print('FAILURE for query', polygon_url_plus)
    return None
  str_response = response.read().decode('utf-8')
  results = literal_eval(str_response.replace('true', 'True').replace('false', 'False'))['results']
  if print_results:
    for s in results:
      print(s)
  return results

def _date_to_str(d):
  return d.strftime('%Y-%m-%d')

def _stock_query(stock_ticker, first_date, last_date):
  # see Aggregates (Bars) in https://polygon.io/docs/stocks/ws_stocks_t
  result_raw = _run_polygon_query_and_process_results(
    f"v2/aggs/ticker/{stock_ticker}/range/1/day/{_date_to_str(first_date)}/{_date_to_str(last_date)}?",
    print_results=False)

  result = pd.DataFrame({
    price_code: [r[price_code] for r in result_raw]
    for price_code in zip(('c', 'h', 'l', 'o', 'vw', 'v'), ('open', 'close', 'high', 'low', 'average', 'volume'))
                        }, index=pd.DatetimeIndex([datetime.fromtimestamp(r['t'] / 1000.) for r in result_raw]))

  return result

def all_stocks_query(date=None, price_code='c', **kwargs):
  # see Aggregates (Bars) in https://polygon.io/docs/stocks/ws_stocks_t
  assert price_code in ['c', 'h', 'l', 'o', 'vw']
  if date is None:
    date = date.today()
  _run_polygon_query_and_process_results(
    f"v2/aggs/grouped/locale/global/market/stocks/{_date_to_str(date)}?adjusted=true&include_otc=true&",
    **kwarg)


def __all_tickers_query(market='', **kwargs):
  results = _run_polygon_query_and_process_results(
    f"v3/reference/tickers?exchange=XFRA&market={market}&active=true&limit=1000&",
    **kwargs)
  locales = {}
  for r in results:
    locales[r['locale']] = None
  print(locales.keys())


#stock_query(stock_ticker='AAPL')
#all_stocks_query(None)
#all_tickers_query('indices', print_results=False)
