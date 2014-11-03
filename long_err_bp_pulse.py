
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

df_all = pd.DataFrame()
for response_file in response_files:
    print(response_file)
    data = read_into_dataframe(response_file)
    
    col_of_interest = ['estm_orig', 'participant_response', 'condition_number', 'bp_d', 'bp_s', 'pulse']
    data_of_interest = data[col_of_interest]
    # print(data_of_interest.head(20))
    data_of_interest['abs_error'] = abs(data_of_interest['estm_orig'] - data_of_interest['participant_response'])

    
    data_with_group = pd.concat([data_of_interest, generate_sections()], axis=1)

    avg_abs_error = pd.DataFrame(data_with_group.groupby('section_number').agg({
        'abs_error':np.mean
        }))

    data_drop_na = data_with_group
    data_drop_na = data_drop_na.dropna()[['condition_number', 'bp_d', 'bp_s', 'pulse', 'section_number']]

    avg_abs_error.index.name = 'section_number'
    avg_abs_error.reset_index(inplace=True)
    data_merged = pd.merge(avg_abs_error, data_drop_na, on='section_number')

    colnames = data_merged.columns
    df = pd.DataFrame([[response_files[0].split('.')[0], data_merged.at[0, 'condition_number']]],
                      columns=['participant', 'condition'])
    for line in data_merged.iterrows():
        line_data = {}
        # print(line)
        section_number = str(int(line[1][0]))
        # print('section number: ', section_number)

        abs_error_key = 'abs_error_' + section_number
        abs_error_value = line[1][1]
        # print('abs_error_key: ', abs_error_key,' ; abs_error_value: ', abs_error_value)

        bp_d_key = 'bp_d_' + section_number
        bp_d_value = line[1][3]
        # print('bp_d_key: ', bp_d_key,' ; bp_d_value: ', bp_d_value)

        bp_s_key = 'bp_s_' + section_number
        bp_s_value = line[1][4]
        # print('bp_s_key: ', bp_s_key,' ; bp_s_value: ', bp_s_value)

        pulse_key = 'pulse_' + section_number
        pulse_value = line[1][5]
        # print('pulse_key: ', pulse_key,' ; pulse_value: ', pulse_value)

        row_df = pd.DataFrame([[abs_error_value, bp_d_value, bp_s_value, pulse_value]],
                              columns=[abs_error_key, bp_d_key, bp_s_key, pulse_key])
        df = pd.concat([df, row_df],axis=1)
    df_all = df_all.append(df)
df_all


# In[ ]:

df_all.to_csv("bp_pulse.csv")


# In[ ]:

# this is a test block before loop
print(response_files[1])
data = read_into_dataframe(response_files[1])

col_of_interest = ['estm_orig', 'participant_response', 'condition_number', 'bp_d', 'bp_s', 'pulse']
data_of_interest = data[col_of_interest]
data_of_interest['abs_error'] = abs(data_of_interest['estm_orig'] - data_of_interest['participant_response'])

data_with_group = pd.concat([data_of_interest, generate_sections()], axis=1)

avg_abs_error = pd.DataFrame(data_with_group.groupby('section_number').agg({
    'abs_error':np.mean
    }))

data_drop_na = data_with_group
data_drop_na = data_drop_na.dropna()[['condition_number', 'bp_d', 'bp_s', 'pulse', 'section_number']]

avg_abs_error.index.name = 'section_number'
avg_abs_error.reset_index(inplace=True)
data_merged = pd.merge(avg_abs_error, data_drop_na, on='section_number')

colnames = data_merged.columns
df = pd.DataFrame([[response_files[0].split('.')[0], data_merged.at[0, 'condition_number']]],
                  columns=['participant', 'condition'])

for line in data_merged.iterrows():
    line_data = {}
    # print(line)
    section_number = str(int(line[1][0]))
    # print('section number: ', section_number)
    
    abs_error_key = 'abs_error_' + section_number
    abs_error_value = line[1][1]
    # print('abs_error_key: ', abs_error_key,' ; abs_error_value: ', abs_error_value)
    
    bp_d_key = 'bp_d_' + section_number
    bp_d_value = line[1][3]
    # print('bp_d_key: ', bp_d_key,' ; bp_d_value: ', bp_d_value)
    
    bp_s_key = 'bp_s_' + section_number
    bp_s_value = line[1][4]
    # print('bp_s_key: ', bp_s_key,' ; bp_s_value: ', bp_s_value)
    
    pulse_key = 'pulse_' + section_number
    pulse_value = line[1][5]
    # print('pulse_key: ', pulse_key,' ; pulse_value: ', pulse_value)
    
    row_df = pd.DataFrame([[abs_error_value, bp_d_value, bp_s_value, pulse_value]],
                          columns=[abs_error_key, bp_d_key, bp_s_key, pulse_key])
    df = pd.concat([df, row_df],axis=1)
df
#data_merged.pivot('section_number', 'condition_number', 'abs_error')

