import pandas as pd
def get_stock_exchange_info():
  df = pd.read_csv(
    'https://www.iso20022.org/sites/default/files/ISO10383_MIC/ISO10383_MIC.csv',
    encoding='ISO8859-1')
  #selection = df.loc[df['CITY'] == 'FRANKFURT']
  #a = selection['MARKET NAME-INSTITUTION DESCRIPTION'].unique()
  a = df[df['MARKET NAME-INSTITUTION DESCRIPTION'].str.contains(
    "DEUTSCHE BOERSE AG")]
  print(a)
  return
  a.sort()
  for _a in a:
    print(_a)


#get_stock_exchange_info()