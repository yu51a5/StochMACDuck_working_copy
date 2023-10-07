import pandas as pd
from settings import excel_filename, info_filename, last_date_filename
from auxiliary import datetime_now

def save_number_files(last_date_data, history_indicators):

  info = 'Prices and Indicators obtained by StochMACDuck ' + datetime_now()
  
  with open(info_filename + '.txt', "w") as text_file:
    text_file.write(info)
    
  last_date_data.to_csv(last_date_filename + '.csv') 

  with open(last_date_filename + '.txt', "w") as text_file:
    text_file.write(last_date_data.to_string())
  
  with pd.ExcelWriter(excel_filename) as writer:  
    info_df = pd.DataFrame([[info]], index=[' '], columns=[' ']) 
    info_df.to_excel(writer, sheet_name='Info')
  
  with pd.ExcelWriter(excel_filename, mode='a') as writer:  
    last_date_data.to_excel(writer, sheet_name='Summary')
    for ticker, values in history_indicators.items():
      values.to_excel(writer, sheet_name=ticker, index=False)
