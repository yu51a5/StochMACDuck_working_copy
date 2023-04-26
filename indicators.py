import pandas as pd
import pandas_ta
from settings import indicator_name_parameters
from auxiliary import get_tail_of_a_column

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
  signal_2 = get_tail_of_a_column(df, column_name='signal', how_many=2)

  stoch_distance = -abs(50. - stochD)
  signal_diff = 0. if signal_2[0] * signal_2[1] >= 0. else (signal_2[0] - signal_2[1])
  
  result = [signal_diff, stoch_distance if stoch_distance < 40. else 0., stoch_distance]
  return result
  
############################################################################

def compute_indicators_and_summary(all_tickers, history_indicators):
  ind_title = {}
  for ticker in all_tickers:
    for indicator_name, indicator_parameters in indicator_name_parameters.items():
      ind_function = indicator_curves[indicator_name]['function']
      ind_title[indicator_name], _ = ind_function(history_indicators[ticker],
                                                  **indicator_parameters)
  history_indicators = dict(sorted(history_indicators.items(), key=lambda item: stochD_sorting_function(item[1])))
  
  ############################################################################  
  pd_dct = {ticker : history_indicators[ticker].tail(1) for ticker in history_indicators.keys()}
  
  last_date_data = pd.concat(pd_dct, axis=0).reset_index(level=0).rename({'level_0':'ticker'}, axis=1)
  last_date_data = last_date_data.reset_index()
  last_date_data = last_date_data.set_index('ticker')
  last_date_data = last_date_data.drop('Date', axis=1)
  
  indicator_info = {ind_name: {'title' : ind_title[ind_name]} for ind_name in indicator_curves.keys()}
  
  return history_indicators, last_date_data, indicator_info
  