import pandas as pd
from settings import excel_filename, info_filename, last_date_filename, tickers_long_names_filename, unnecessary_column_names
from auxiliary import datetime_now

def save_number_files(last_date_data, info, history_indicators):

  info_line = 'Prices and Indicators obtained by StochMACDuck ' + datetime_now()
  
  with open(info_filename + '.txt', "w") as text_file:
    text_file.write(info_line)
    
  last_date_data.to_csv(last_date_filename + '.csv') 

  with open(last_date_filename + '.txt', "w") as text_file:
    text_file.write(last_date_data.to_string())

  with open(last_date_filename + '.txt', "w") as text_file:
    # ticker_only_country_list = get_ticker_only_country_list(all_tickers)
    links = [] #[f'https://www.marketwatch.com/investing/stock/{ticker}/charts?countryCode=UK' for ticker_only, country in all_tickers ]
    # text_file.write('\n'.join(links))

  for t in info:
    columns = [k for k in info[t].keys()]
    break
  tickers_long_names_pd = pd.DataFrame( [info_one_ticker.values() for info_one_ticker in info.values()], index=info.keys(), columns=columns)
  tickers_long_names_pd.index.name = 'Ticker'

  assert tickers_long_names_pd.index.sort_values().equals(last_date_data.index.sort_values())

  long_table = pd.concat([tickers_long_names_pd, last_date_data], axis=1)
  unnecessary_columns = long_table.filter(items=unnecessary_column_names)
  unnecessary_columns['Data Date'] = pd.to_datetime(unnecessary_columns['Data Date'])
  max_date = unnecessary_columns['Data Date'].max()
  print(unnecessary_columns.loc[unnecessary_columns['Data Date'] < max_date])
  print('Dividends', unnecessary_columns.loc[not(unnecessary_columns['Dividends'].isna()  or (abs(unnecessary_columns['Dividends'])< 1E-8))])
  print('Stock Splits', unnecessary_columns.loc[not(unnecessary_columns['Stock Splits'].isna()  or (abs(unnecessary_columns['Stock Splits'])< 1E-8))])
  print('Capital Gains', unnecessary_columns.loc[not(unnecessary_columns['Capital Gains'].isna()  or (abs(unnecessary_columns['Capital Gains'])< 1E-8))])
  
  print('unnecessary_columns', unnecessary_columns.dtypes, unnecessary_columns.columns)
  print(unnecessary_columns)
  long_table.drop(columns=unnecessary_column_names, inplace=True)
    
  assert tickers_long_names_pd.index.sort_values().equals(long_table.index.sort_values())
  
  with open(tickers_long_names_filename + '.txt', "w") as text_file:
    text_file.write(long_table.to_string())
  with pd.ExcelWriter(tickers_long_names_filename + '.xlsx') as writer:
    long_table.to_excel(writer, sheet_name='TickersInfo')

  assert tickers_long_names_pd.index.equals(long_table.index)
  
  with pd.ExcelWriter(excel_filename) as writer:  
    info_df = pd.DataFrame([[info]], index=[' '], columns=[' ']) 
    info_df.to_excel(writer, sheet_name='Info')
  
  with pd.ExcelWriter(excel_filename, mode='a') as writer:  
    last_date_data.to_excel(writer, sheet_name='Summary')
    for ticker, values in history_indicators.items():
      values.to_excel(writer, sheet_name=ticker, index=False)


#pd.concat([df1, df2], axis=1)
