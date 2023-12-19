from datetime import timedelta

from matplotlib_plotting import plot_prices_and_indicators

from settings import all_tickers, how_many_days_to_plot, last_date, how_many_calendar_days_of_data_to_fetch, max_qty_assets_to_plot
from auxiliary import time_now
from yfinance_queries import stock_query
from indicators import compute_indicators_and_summary
from number_files import save_number_files


############################################################################
history_indicators = {}
info = {}
current_prices = {}
dividends = {}
splits = {}
print('\nStarted to fetch data ' + time_now())
first_date = last_date - timedelta(days=how_many_calendar_days_of_data_to_fetch)
not_found = []
for ticker in all_tickers:
  info[ticker], history_indicators[ticker], dividends[ticker], splits[ticker] = stock_query(stock_ticker=ticker, last_date=last_date, first_date=first_date)
  if not info[ticker]:
    not_found.append(ticker)
    del info[ticker]
    del history_indicators[ticker]
    del dividends[ticker]
    del splits[ticker]
    print(f"Could not find any information about {ticker}")
  else:
    print(f"{ticker} ({', '.join([key + ': ' + str(value) for key, value in info[ticker].items()])}): {history_indicators[ticker].shape[0]} data points")
  
print(f'Finished fetching data for {len(all_tickers)} tickers {time_now()}')

############################################################################
print('\nStarted computing indicators ' + time_now())

history_indicators, last_date_data, indicator_info, problems_df = compute_indicators_and_summary(info, history_indicators, dividends, splits)
print(last_date_data)

print('Finished computing indicators ' + time_now())  

############################################################################
save_number_files(last_date_data=last_date_data, history_indicators=history_indicators, problems=problems_df)

############################################################################
print(
  '\nStarted to plot ' + time_now() + '. It could take a couple of minutes.',
  '\nOnce there is a "Completed" message right below this line, you can download the jpg file that displays the plots.'
)
what_to_plot = {}

for q, (ticker, values) in enumerate(history_indicators.items()):
  if q == max_qty_assets_to_plot:
    break
  values_to_plot = values.tail(how_many_days_to_plot) if isinstance(how_many_days_to_plot, int) else values
  what_to_plot[ticker] = (values_to_plot, info[ticker])
    
plot_prices_and_indicators(what_to_plot, indicator_info)

print(f'Completed {time_now()}!')
