from datetime import datetime

def time_now():
  result = 'at ' + str(datetime.now())[11:19]
  return result

def datetime_now():
  now_ = str(datetime.now())
  result = 'on ' + now_[:10] + ' at ' + now_[11:19]
  return result

def get_tail_of_a_column(df, column_name, how_many=1):
  tail = df.tail(how_many)
  column_index = tail.columns.get_loc(column_name)
  result = tail.iloc[0, column_index] if how_many == 1 else [tail.iloc[how_many-1-h, column_index] for h in range(how_many)]
  return result
