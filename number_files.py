import pandas as pd
from settings import excel_filename
from auxiliary import datetime_now

def save_number_files(last_date_data, history_indicators):
  info_df = pd.DataFrame([['Prices and Indicators obtained by StochMACDuck ' + datetime_now()]],
                         index=[' '], columns=[' ']) 
  
  with pd.ExcelWriter(excel_filename) as writer:  
    info_df.to_excel(writer, sheet_name='Info')
  
  with pd.ExcelWriter(excel_filename, mode='a') as writer:  
    last_date_data.to_excel(writer, sheet_name='Summary')
    for ticker, values in history_indicators.items():
      values.to_excel(writer, sheet_name=ticker, index=False)
