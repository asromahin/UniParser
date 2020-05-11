import pandas as pd
import src.utils.pd_utils as pd_utils

import time

#print('good' - 'goo')

df = pd.read_csv('res.csv')

start_time = time.time()
df = pd_utils.filter_empty(df)
print(time.time()-start_time, len(df.keys()))

start_time = time.time()
df = pd_utils.filter_long(df)
print(time.time()-start_time, len(df.keys()))

start_time = time.time()
df = pd_utils.filter_simple_columns(df)
print(time.time()-start_time, len(df.keys()))

df.to_csv('res2.csv')
