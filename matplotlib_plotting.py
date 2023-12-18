import matplotlib.pyplot as plt
import math 
import pandas as pd

from settings import plot_height_inches, chart_color, plot_filename, max_digits_for_price, max_title_length
from auxiliary import datetime_now
from indicators import indicator_curves

############################################################################
def plot_prices_and_indicators(history_indicators, indicator_info):
  if not history_indicators:
    print("empty history_indicators")
    return
  stock_qty = len(history_indicators)

  fig, axes = plt.subplots(1+len(indicator_curves), stock_qty, sharex=False, gridspec_kw={'hspace': 0})
  fig.suptitle('  Prices and Indicators plotted by StochMACDuck ' + datetime_now(), x=0, ha='left')
  for i, (ticker, (prices_df_2, info_ticker)) in enumerate(history_indicators.items()):
    _candle_plot(ax=axes[0][i], ticker=ticker, prices=prices_df_2, info=info_ticker)
    for iic, indicator in enumerate(indicator_info.keys()):
      for ind_curve_name in indicator_curves[indicator]['curves']:
        if ind_curve_name not in prices_df_2:
          continue
        if ind_curve_name == 'histogram':
          axes[1+iic][i].bar(x=prices_df_2.index, height=prices_df_2[ind_curve_name], **get_style(curve_name=ind_curve_name))
        else:
          axes[1+iic][i].plot(prices_df_2.index, prices_df_2[ind_curve_name], **get_style(curve_name=ind_curve_name))
        
        axes[1+iic][i].set_ylabel(indicator_info[indicator]['title'], fontsize=8)
      if indicator == 'Stochastic':
        axes[1+iic][i].set_ylim(bottom=0., top=100.)
  for h in range(stock_qty):
    for v in range(len(indicator_curves)):
      axes[v][h].set_xticklabels([])
    _rotate_xticks(axes[-1][h])

  fig.set_size_inches(0.8 * stock_qty * plot_height_inches, plot_height_inches)
  fig.tight_layout()
  fig.savefig(plot_filename)
  fig.show()

############################################################################
def _rotate_xticks(ax, angle=45):
  ax.set_xticks(ax.get_xticks())
  ax.set_xticklabels(ax.get_xticklabels(), rotation=angle, ha='right')

############################################################################
def get_style(curve_name):
  if isinstance(chart_color[curve_name], str):
    return {'color' : chart_color[curve_name]}
  return {'color' : chart_color[curve_name][0], 'linestyle' : chart_color[curve_name][1]}

############################################################################
def _candle_plot(ax, ticker, prices, info, width1=.8, width2=.1):
  # source: https://www.statology.org/matplotlib-python-candlestick-chart/
  #plot up prices
  up = prices[prices.close >= prices.open]
  down = prices[prices.close < prices.open]
  for up_or_down, curve_name in [[up, 'stock_green'], [down, 'stock_red']]:
    max_co = up.close if up_or_down is up else down.open
    min_co = up.open if up_or_down is up else down.close
    for bottom, top, width in zip((up_or_down.open, max_co, min_co),
                                  (up_or_down.close, up_or_down.high, up_or_down.low),
                                  (width1, width2, width2)):
      ax.bar(up_or_down.index,
             top - bottom,
             width,
             bottom=bottom,
             **get_style(curve_name=curve_name))

  ax.plot(prices.index, prices.close, **get_style(curve_name='stock_mid'), zorder=-.1)

  #rotate x-axis tick labels
  #_rotate_xticks(ax)
  for i in range(len(prices.index)):
    last_close = prices["close"].iloc[-1-i]
    if not pd.isna(last_close):
      break
  int_digits_qty = math.floor(math.log10(last_close)) + 1
  rounded_last_close = round(last_close, max(0, max_digits_for_price - int_digits_qty))
  title = f'{ticker} ({info["currency"]} {rounded_last_close}, {info["longName"]})'
  ax.set_title(title[:max_title_length])
  ax.set_ylabel('Prices')
  