import os
import shutil
import pandas as pd
from settings import folder_for_files, excel_filename, tickers_long_names_filename
from auxiliary import datetime_now

def print_all_formats(df, filename, excel_sheet_name=None, more_excel_data={}):
  _filename = os.path.join(folder_for_files, filename)
  df.to_csv(_filename + '.csv') 
  with open(_filename + '.txt', "w") as text_file:
    text_file.write(df.to_string())
  #with pd.ExcelWriter(_filename + '.xlsx') as writer:
  #  df.to_excel(writer, sheet_name=excel_sheet_name if excel_sheet_name else filename)
  #  for sheet_name, (data_df, do_index) in more_excel_data.items():
  #     pass #data_df.to_excel(writer, sheet_name=sheet_name, index=do_index)
      
  return _filename

def save_number_files(last_date_data, history_indicators, problems):
  
  if os.path.isdir(folder_for_files):
    shutil.rmtree(folder_for_files)

  os.mkdir(folder_for_files)
  os.mkdir(os.path.join(folder_for_files, 'by_ticker'))

  info_line = 'Prices and Indicators obtained by StochMACDuck ' + datetime_now()

  #with open(last_date_filename + '.txt', "w") as text_file:
    # ticker_only_country_list = get_ticker_only_country_list(all_tickers)
    #links = [] #[f'https://www.marketwatch.com/investing/stock/{ticker}/charts?countryCode=UK' for ticker_only, country in all_tickers ]
    # text_file.write('\n'.join(links))

  if len(problems):
    print_all_formats(df=problems, filename='problems')
  else:
    print("NO BAD ROWS")
  print_all_formats(last_date_data, filename=tickers_long_names_filename)
  
  info_df = pd.DataFrame([[info_line]], index=[' '], columns=[' '])
  print_all_formats(info_df, filename=excel_filename)

  for ticker, values in history_indicators.items():
    print_all_formats(df=values, filename=os.path.join('by_ticker', ticker))


#pd.concat([df1, df2], axis=1)
