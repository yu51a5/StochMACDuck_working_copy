import pandas as pd
from settings import folder_for_files, excel_filename, info_filename, last_date_filename, tickers_long_names_filename, unnecessary_column_names
from auxiliary import datetime_now
from indicators import stochD_sorting_function

def print_all_formats(df, filename):
  _filemame = os.path.join(folder_for_files, filename)
  df.to_csv(l_filename + '.csv') 
  with open(_filemame + '.txt', "w") as text_file:
    text_file.write(df.to_string())
  with pd.ExcelWriter(_filemame + '.xlsx') as writer:
    df.to_excel(writer, sheet_name=filemame)

def save_number_files(last_date_data, info, history_indicators):

  info_line = 'Prices and Indicators obtained by StochMACDuck ' + datetime_now()
  
  with open(info_filename + '.txt', "w") as text_file:
    text_file.write(info_line)

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
  bad_rows = unnecessary_columns['Data Date'] < max_date
  for what in unnecessary_columns.columns[:-3]:
    bad_rows = (bad_rows) | (~((unnecessary_columns[what].isna()) | (abs(unnecessary_columns[what])< 1E-8)))
  if bad_rows.any():
    problems = unnecessary_columns.loc[bad_rows]
    print_all_formats(df=problems, filename='problems')
  else:
    print("NO BAD ROWS")
  
  long_table.drop(columns=unnecessary_columns.columns, inplace=True)
  long_table.sort_index(inplace=True, key=lambda key: stochD_sorting_function(history_indicators[key.str]))
  #.sort_values(by, *, axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last', ignore_index=False, key=None)
  print_all_formats(long_table=problems, filename=tickers_long_names_filename)
  
  assert tickers_long_names_pd.index.equals(long_table.index)
  
  with pd.ExcelWriter(excel_filename) as writer:  
    info_df = pd.DataFrame([[info]], index=[' '], columns=[' ']) 
    info_df.to_excel(writer, sheet_name='Info')
  
  with pd.ExcelWriter(excel_filename, mode='a') as writer:  
    last_date_data.to_excel(writer, sheet_name='Summary')
    for ticker, values in history_indicators.items():
      values.to_excel(writer, sheet_name=ticker, index=False)


#pd.concat([df1, df2], axis=1)
