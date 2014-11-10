
# coding: utf-8

# In[ ]:

import pandas as pd
import numpy as np
import glob


# In[ ]:

response_files = glob.glob("*.txt")
response_files


# In[ ]:

def data_set_column_names():
    colnames = ['time', 'orgi_trial', 'adv', 'mksh', 'revg', 'price_d', 'price_r', 'estm_orig', 'time_r', 
                'participant_response', 'condition_number', 
                'bp_s', 'bp_d', 'pulse']
    assert isinstance(colnames, list)
    return colnames


# In[ ]:

def read_into_dataframe(response_file):
    return pd.read_csv(response_file, names = data_set_column_names())


# In[ ]:

def generate_sections():
    my_list = []
    for i in range(12):
        for j in range(15):
            my_list.append(i)
    assert len(my_list) == 180
    return pd.DataFrame(my_list, columns=['section_number'])


# In[ ]:

def get_dataframe(response_file):
    data = read_into_dataframe(response_file)
    data = data.applymap(lambda x: np.nan if x == "None" else x)
    return data


# In[ ]:

def get_cols_of_interest(df):
    col_of_interest = ['price_r', 'participant_response', 'condition_number', 'bp_d', 'bp_s', 'pulse']
    assert isinstance(col_of_interest, list)
    data_of_interest = df[col_of_interest]
    return data_of_interest


# In[ ]:

def clean_dataframe(df):
    df['abs_error'] = abs(df['price_r'].astype(float) - df['participant_response'].astype(float))
    
    data_with_group = pd.concat([df, generate_sections()], axis=1)

    # get average error per section
    # avg_abs_error = pd.DataFrame(data_with_group.groupby('section_number').agg({'abs_error':np.mean}))
    # avg_abs_error = pd.DataFrame(data_with_group.groupby('section_number').mean())

    # aet condition number, bp, pulse and section number
    data_drop_na = data_with_group
    data_drop_na = data_drop_na.dropna()[['condition_number', 'bp_d', 'bp_s', 'pulse', 'section_number']]

    # concatenate the average time by ending time results
    # avg_abs_error.index.name = 'section_number'
    # avg_abs_error.reset_index(inplace=True)
    
    # data_merged = pd.merge(avg_abs_error, data_drop_na, on='section_number')
    # return data_merged
    return data_drop_na


# In[ ]:

def get_totals(response_file):
    df = get_dataframe(response_file)
    df = get_cols_of_interest(df)
    df['abs_error'] = abs(df['price_r'].astype(float) - df['participant_response'].astype(float))
    sum_abs_error = df['abs_error'].astype(float).sum(axis=2)
    sum_obs = df['participant_response'].count()
    return sum_abs_error, sum_obs


# In[ ]:

df_all = pd.DataFrame()
for response_file in response_files:
    df = get_dataframe(response_file)
    df = get_cols_of_interest(df)
    # df = clean_dataframe(df)
    df['respondent'] = response_file
    # total_abs_error, total_abs_obs = get_totals(response_file)
    # df['total_abs_error'], df['total_abs_obs'] = total_abs_error, total_abs_obs
    df_all = df_all.append(df)
df_all


# In[ ]:

df_all.to_csv("stacked.csv")

