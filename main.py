from matplotlib_plotting import plot_prices_and_indicators

from settings import all_tickers, how_many_days_to_plot, last_date, how_many_calendar_days_of_data_to_fetch, max_qty_assets_to_plot
from auxiliary import time_now
from stock_queries import stock_query
from indicators import compute_indicators_and_summary
from number_files import save_number_files

############################################################################
history_indicators = {}
print('\nStarted to fetch data ' + time_now())
for ticker in all_tickers:
  history_indicators[ticker] = stock_query(stock_ticker=ticker, last_date=last_date, how_many_calendar_days_of_data_to_fetch=how_many_calendar_days_of_data_to_fetch)
  print(f"{ticker}: {history_indicators[ticker].shape[0]} data points")
  
print(f'Finished fetching data for {len(all_tickers)} tickers {time_now()}')

############################################################################
print('\nStarted to compute indicators ' + time_now())

history_indicators, last_date_data, indicator_info = compute_indicators_and_summary(all_tickers, history_indicators)
print(last_date_data)

print('Finished computing indicators ' + time_now())  

############################################################################
save_number_files(last_date_data=last_date_data, history_indicators=history_indicators)

############################################################################
print(
  '\nStarted to plot ' + time_now(),
  '\nIf it takes a while AND CPU and RAM - see the bottom left corner of the screen - are both idle, reload your browser window'
)
what_to_plot = {}
q = 0
for ticker, values in history_indicators.items():
  what_to_plot[ticker] = values.tail(how_many_days_to_plot) if isinstance(how_many_days_to_plot, int) else values
  q += 1
  if q == max_qty_assets_to_plot:
    break
plot_prices_and_indicators(what_to_plot, indicator_info)
