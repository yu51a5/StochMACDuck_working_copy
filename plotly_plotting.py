import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

chart_color = {'stochd' : 'blue', 'stochk' : 'red',
                 'movingaverageconvergencedivergence' : 'orange', 'signal' : 'cyan', 'histogram': 'black'}


def plot_stock(history_indicators, how_many_days=30 ):
  if not history_indicators:
    print("empty history_indicators")
    return
  nb_cols = len(history_indicators)
  nb_rows = 2 + max([len(v['indicators']) for v in history_indicators.values() if 'indicators' in v] + [0]) 
  fig = make_subplots(cols=nb_cols, rows=nb_rows, 
                      subplot_titles=[(["?"] * nb_rows) for _ in range(nb_cols)] if nb_rows > 2 else ["?"] * nb_cols)
  
  for iti, history_indicators_ticker in enumerate(history_indicators.values()):

    dates_this_asset = history_indicators_ticker['dates'][-how_many_days:]
    
    fig.add_candlestick(x=dates_this_asset,
                        **{s: history_indicators_ticker['prices'][s[0].lower()][-how_many_days:] 
                                for s in ('open', 'high', 'low', 'close')},
                        col=1+iti, row=1)

    indicators_this_assets = history_indicators_ticker['indicators'] if 'indicators' in history_indicators_ticker else {}
    for i, asset_indicators in enumerate(indicators_this_assets):
      for ind_name, (ind_title, ind_values) in asset_indicators.items():
        kwargs = dict(x=dates_this_asset, y=ind_values[-how_many_days:], col=1+iti, row=3+i)
        if ind_name == 'histogram':
          fig.add_bar(**kwargs, marker={'color': 'black'})
        else:
          fig.add_scatter(**kwargs, line={'color' : chart_color[ins]})
  
  fig.update_layout(width=400*nb_cols, height=250*nb_rows, showlegend=False)
  fig.show()