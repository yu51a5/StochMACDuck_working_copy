import pandas as pd
import numpy as np
import pandas_ta
from settings import indicator_name_parameters
from auxiliary import get_tail_of_a_column
from datetime import datetime

############################################################################
# https://stackoverflow.com/questions/48775841/pandas-ema-not-matching-the-stocks-ema
def calc_MACD(prices, fast=12, slow=26, signal_period=9):

  result = pandas_ta.momentum.macd(close=prices.close,
                                   fast=fast,
                                   slow=slow,
                                   signal=signal_period)

  suffix = f'_{fast}_{slow}_{signal_period}'
  prices['MACD'] = result[f'MACD{suffix}']
  prices['signal'] = result[f'MACDs{suffix}']
  prices['histogram'] = result[f'MACDh{suffix}']

  title = f'MACD(f={fast}, sl={slow}, sig={signal_period})'
  return title, prices

############################################################################
def calc_stoch(prices, period=3, k_period=14, level_bottom=None, level_top=None):
  title = f'Stoch(k={k_period}, d={period})'  # , slowing={sto_period}
  
  #https://www.investopedia.com/terms/s/stochasticoscillator.asp
  result = pandas_ta.momentum.stoch(high=prices.high,
                                    low=prices.low,
                                    close=prices.close,
                                    window=k_period,
                                    smooth_window=period)
  prices['stochK'] = result[f'STOCHk_{k_period}_{period}_{period}']
  prices['stochD'] = result[f'STOCHd_{k_period}_{period}_{period}']
  prices['level_bottom'] = level_bottom
  prices['level_top'] = level_top
  
  return title, prices

############################################################################
indicator_curves = {
  'MACD': {
    'curves': ['MACD', 'signal', 'histogram'],
    'function': calc_MACD
  },
  'Stochastic': {
    'curves': ['stochD', 'stochK', 'level_bottom', 'level_top'],
    'function': calc_stoch
  }
}

############################################################################
def stochD_sorting_function(df):
  stochD = get_tail_of_a_column(df, column_name="stochD")
  histogram_ = get_tail_of_a_column(df, column_name='histogram', how_many=2)

  stoch_distance = -abs(50. - stochD)
  histogram_diff = 0. if histogram_[0] * histogram_[1] >= 0. else -abs(histogram_[0] - histogram_[1])
  
  result = [stoch_distance if stoch_distance < -40. else 0., histogram_diff, stoch_distance]
  return result
  
############################################################################

def compute_indicators_and_summary(info, history_indicators):
  ind_title = {}
  for ticker in info:
    for indicator_name, indicator_parameters in indicator_name_parameters.items():
      ind_function = indicator_curves[indicator_name]['function']
      ind_title[indicator_name], _ = ind_function(history_indicators[ticker]['history'],
                                                  **indicator_parameters)
  #history_indicators = dict(sorted(history_indicators.items(), key=lambda item: stochD_sorting_function(item[1])))
  
  ############################################################################  
  flat_tails = {}

  multiindex = pd.MultiIndex(levels=[[],[],[]],
                            codes=[[],[],[]],
                           names={'Ticker': str, 'Date': datetime, 'Value Name': str})

  problems_df = pd.DataFrame(columns={'Problem value' : float, 'Long name'  : str}, 
                             index = multiindex)

  for ticker, all_dates_df in history_indicators.items():
    for date, row in all_dates_df['history'].iterrows():
      for what in all_dates_df['history'].columns:
        value = row[what]
        if (pd.isna(value)) or (value < 1E-8):
          problems_df.loc[(ticker, date, what), :] =  pd.Series({'Long name' : info[ticker]['longName'], 'Problem value' : value})
    for what in ['Dividends', 'Stock Splits']:
      for date, row in all_dates_df[what].iterrows():
        problems_df.loc[(ticker, date, what), :] =  pd.Series({'Long name' : info[ticker]['longName'], 'Problem value' : row[0]})

    tail =  all_dates_df['history'].tail(3)
    to_remove = [cn for cn in tail.columns if cn in ['level_bottom', 'level_top', 'Dividends', 'Stock Splits', 'Capital Gains', 'Data Date']]
    tail = tail.drop(columns=to_remove)
    tail = tail.loc[tail.index[::-1]]
    tail.reset_index(inplace=True)
    
    tail_stack = tail.stack()
    # We recommend using DataFrame.to_numpy() instead. https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.values.html
    flat_tails[ticker] = pd.DataFrame([tail_stack.to_numpy()],  columns=[f'{j}-{i}' for i, j in tail_stack.index])


  
  last_date_data = pd.concat(flat_tails, axis=0).reset_index(level=0).rename({'level_0':'ticker'}, axis=1)
  # last_date_data.reset_index(inplace=True)
  last_date_data = last_date_data.set_index('ticker')

  print('last_date_data', last_date_data)
  
  indicator_info = {ind_name: {'title' : ind_title[ind_name]} for ind_name in indicator_curves.keys()}

  for t in info:
    columns = [k for k in info[t].keys()]
    break
  tickers_long_names_pd = pd.DataFrame( [info_one_ticker.values() for info_one_ticker in info.values()], index=info.keys(), columns=columns)
  tickers_long_names_pd.index.name = 'Ticker'

  assert tickers_long_names_pd.index.sort_values().equals(last_date_data.index.sort_values())

  long_table = pd.concat([tickers_long_names_pd, last_date_data], axis=1)

  assert tickers_long_names_pd.index.equals(long_table.index)
  
  #df.sort_index(key=lambda k:k.str[1], inplace=True)
  # long_table.sort_index(key=lambda k:ord(k.str[1]), inplace=True)
  # long_table.sort_index(inplace=True, key=lambda key: stochD_sorting_function(history_indicators[key.str]))
  #.sort_values(by, *, axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last', ignore_index=False, key=None)  
  
  return history_indicators, long_table, indicator_info, problems_df
  