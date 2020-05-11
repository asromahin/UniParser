import pandas as pd

def filter_empty(df):
    res_df = df.copy()
    keys = res_df.keys()
    for key in keys:
        column = res_df[key]
        key_uniq = column.nunique()
        #print(key_uniq)
        if key_uniq <= 1:
            res_df = res_df.drop(key, axis=1)
    return res_df

def filter_long(df, max_length=300):
    res_df = df.copy()
    keys = res_df.keys()
    for key in keys:
        column = res_df[key]
       #print(key, column.dtype)
        if column.dtype == 'object':
            len_max = column.str.len().mean()
            if len_max > max_length:
                res_df = res_df.drop(key, axis=1)
    return res_df

def filter_simple_columns(df):
    res_df = df.copy()
    keys = list(res_df.keys())
    for i in range(0, len(keys)):
        for j in range(i, len(keys)):
            key = keys[i]
            key_to = keys[j]
            column = df[key]
            column_to = df[key_to]
            if key != key_to:
                if column.dtype == 'object' and column_to.dtype == 'object':
                    uniq = (column == column_to).unique()
                    if len(uniq) == 1:
                        if uniq[0] == True:
                            try:
                                res_df = res_df.drop(key, axis=1)
                            except:
                                pass
    return res_df