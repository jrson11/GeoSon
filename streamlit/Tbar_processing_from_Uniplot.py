import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import streamlit as st

'''
# Geotechnics - Tbar processing
Purpose: To extract the first & last Tbar push data from cycles in Uniplot file \n
Author: J.Son, Ph.D., P.E. \n
Last Update: 1/23/2021 \n
'''

# -- Create sidebar for plot controls
st.sidebar.markdown('## Set Nt Parameters')
Nt_und = st.sidebar.slider('Nt undisturbed', 5.0, 15.0, 10.5)  # min, max, default
Nt_rem = st.sidebar.slider('Nt remolded', 5.0, 15.0, 10.5)  # min, max, default

# -- Create upbar to import data
asc_files = st.sidebar.file_uploader('Choose converted CSV files from Uniplot ASC', accept_multiple_files=True)
n_asc = len(asc_files)
#
st.text('Number of ASC files: '+str(n_asc))

def dfTbarfromUniplotCSV(Nt_und,Nt_rem):
    return 0

# Memory allocation
df_TBAR_first = pd.DataFrame()
df_TBAR_last = pd.DataFrame()

for asc_file in asc_files:
    
    df_asc = pd.read_csv(asc_file, skiprows=60)
    cols = df_asc.columns
    
    ii = df_asc[cols[0]] == 'No'
    idx = ii[ii].index.astype(int)[0]
    #st.text(idx)
    df_tbar = df_asc.loc[idx+1:,cols[0:5]]
    df_tbar.columns = ['Rec','Depth_m','Time_s','qT','qT_pull']
        
    # Reset index
    df_tbar.reset_index(inplace=True)
    df_tbar.drop(columns='index', inplace=True)    
    #st.dataframe(df_tbar)
    
    #
    df_tbar.loc[:,'Rec'] = pd.to_numeric(df_tbar.loc[:,'Rec'])
    df_tbar.loc[:,'Depth_m'] = pd.to_numeric(df_tbar.loc[:,'Depth_m'])
    df_tbar.loc[:,'Time_s'] = pd.to_numeric(df_tbar.loc[:,'Time_s'])
    df_tbar.loc[:,'qT'] = pd.to_numeric(df_tbar.loc[:,'qT'])
    df_tbar.loc[:,'qT_pull'] = pd.to_numeric(df_tbar.loc[:,'qT_pull'])
    #st.dataframe(df_tbar)
    #
    df_tbar['qT_MPa'] = np.nan
    ii = df_tbar['qT'].isnull()
    df_tbar.loc[~ii,'qT_MPa'] = df_tbar.loc[~ii,'qT']
    ii = df_tbar['qT_pull'].isnull()
    df_tbar.loc[~ii,'qT_MPa'] = df_tbar.loc[~ii,'qT']
    df_tbar.drop(columns=['qT','qT_pull'], inplace=True)
    
    # Define push & pull to find cycles
    df_tbar['test_type'] = 'push'
    ii = df_tbar.loc[:,'qT_MPa'] < 0
    df_tbar.loc[ii,'test_type'] = 'pull'
    #
    df_tbar['diff'] = (df_tbar.test_type != df_tbar.test_type.shift()).astype(int)
    df_tbar['diff_cumsum'] = df_tbar['diff'].cumsum()
    df_tbar['cycle'] = np.floor((df_tbar['diff_cumsum']-1)/2+1).astype(int)    
    df_tbar.drop(columns=['diff','diff_cumsum'], inplace=True)
    
    # Add location
    loca = asc_file.name.split()[0]
    st.text(loca)
    df_tbar.insert(0,'Loca',loca)
    
    # Fine first and last push only
    ii = df_tbar['cycle'] == 1
    jj = df_tbar['test_type'] == 'push'
    df_tbar_first = df_tbar.loc[ii&jj]
    df_tbar_first.drop(columns=['test_type'], inplace=True)
    #
    ii = df_tbar['cycle'] == max(df_tbar['cycle'])
    jj = df_tbar['test_type'] == 'push'
    df_tbar_last = df_tbar.loc[ii&jj]
    df_tbar_last.drop(columns=['test_type'], inplace=True)
    
    # Calculate Su
    df_tbar_first.insert(df_tbar_first.shape[1],'qT_kPa',df_tbar_first['qT_MPa']*1000)
    df_tbar_first.insert(df_tbar_first.shape[1],'Su_ksf',df_tbar_first['qT_kPa']/Nt_und)
    df_tbar_first['Nt_und'] = Nt_und
    df_tbar_last.insert(df_tbar_last.shape[1],'qT_kPa',df_tbar_last['qT_MPa']*1000)
    df_tbar_last.insert(df_tbar_last.shape[1],'Su_ksf',df_tbar_last['qT_kPa']/Nt_rem)
    df_tbar_last['Nt_rem'] = Nt_rem
    
    # Combine all
    df_TBAR_first = pd.concat([df_TBAR_first,df_tbar_first])    
    df_TBAR_last = pd.concat([df_TBAR_last,df_tbar_last])    
    

## -- Table

st.dataframe(df_TBAR_first)
st.dataframe(df_TBAR_last)




def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv(index=False).encode('utf-8')

csv_first = convert_df(df_TBAR_first)
csv_last = convert_df(df_TBAR_last)

st.sidebar.markdown('## Download the Processing Results')

st.sidebar.download_button(
     label="Download Tbar_first_push as CSV",
     data=csv_first,
     file_name='Tbar_first_push.csv',
     mime='text/csv',
 )
#
st.sidebar.download_button(
     label="Download Tbar_last_push as CSV",
     data=csv_last,
     file_name='Tbar_last_push.csv',
     mime='text/csv',
 )
