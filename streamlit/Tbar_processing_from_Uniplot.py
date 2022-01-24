import numpy as np
import pandas as pd
import streamlit as st

'''
# Geotechnics - Tbar processing
Purpose: To extract the first & last Tbar push data from cycles in Uniplot file \n
Author: J.Son, Ph.D., P.E. \n
Last Update: 1/22/2021 \n
'''

st.sidebar.markdown('## Set Nt Parameters')
iiiiiiiiiii = st.sidebar.slider('Nt undisturbed', 5.0, 15.0, 10.5)  # min, max, default
iiiiiiiiiiii = st.sidebar.slider('Nt remolded', 5.0, 15.0, 10.5)  # min, max, default
iii = st.sidebar.file_uploader('Choose converted CSV files from Uniplot ASC', accept_multiple_files=True)
iiiiiiiiiiiii = len(iii)

'''
## Input files
'''
st.text('Number of ASC files: '+str(iiiiiiiiiiiii))

iiii = pd.DataFrame()
iiiii = pd.DataFrame()

for asc_file in iii:
    
    iiiiii = pd.read_csv(asc_file, skiprows=41, usecols=[0,1,2,3,4])
    cols = iiiiii.columns
    
    ii = iiiiii[cols[0]] == 'No'
    idx = ii[ii].index.astype(int)[0]
    iiiiiii = iiiiii.loc[idx+1:,cols[0:5]]
    iiiiiii.columns = ['Rec','Depth_m','Time_s','qT','qT_pull']
        
    iiiiiii.reset_index(inplace=True)
    iiiiiii.drop(columns='index', inplace=True)    
    
    #
    iiiiiii.loc[:,'Rec'] = pd.to_numeric(iiiiiii.loc[:,'Rec'])
    iiiiiii.loc[:,'Depth_m'] = pd.to_numeric(iiiiiii.loc[:,'Depth_m'])
    iiiiiii.loc[:,'Time_s'] = pd.to_numeric(iiiiiii.loc[:,'Time_s'])
    iiiiiii.loc[:,'qT'] = pd.to_numeric(iiiiiii.loc[:,'qT'])
    iiiiiii.loc[:,'qT_pull'] = pd.to_numeric(iiiiiii.loc[:,'qT_pull'])
    #
    iiiiiii['qT_MPa'] = np.nan
    ii = iiiiiii['qT'].isnull()
    iiiiiii.loc[~ii,'qT_MPa'] = iiiiiii.loc[~ii,'qT']
    ii = iiiiiii['qT_pull'].isnull()
    iiiiiii.loc[~ii,'qT_MPa'] = iiiiiii.loc[~ii,'qT_pull']
    iiiiiii.drop(columns=['qT','qT_pull'], inplace=True)
    
    if iiiiiii.loc[0,'qT_MPa'] < 0:
        iiiiiii.loc[0,'qT_MPa'] = 0
    
    iiiiiii['test_type'] = 'push'
    ii = iiiiiii.loc[:,'qT_MPa'] < 0
    iiiiiii.loc[ii,'test_type'] = 'pull'
    #
    iiiiiii['diff'] = (iiiiiii.test_type != iiiiiii.test_type.shift()).astype(int)
    iiiiiii['diff_cumsum'] = iiiiiii['diff'].cumsum()
    iiiiiii['cycle'] = np.floor((iiiiiii['diff_cumsum']-1)/2+1).astype(int)    
    iiiiiii.drop(columns=['diff','diff_cumsum'], inplace=True)
    st.dataframe(iiiiiii)
    iiiiiiii = asc_file.name.split()[0]
    st.text(iiiiiiii)
    iiiiiii.insert(0,'Loca',iiiiiiii)
    
    ii = iiiiiii['cycle'] == 1
    jj = iiiiiii['test_type'] == 'push'
    iiiiiii_first = iiiiiii.loc[ii&jj]
    iiiiiii_first.drop(columns=['test_type'], inplace=True)
    #
    ii = iiiiiii['cycle'] == max(iiiiiii['cycle'])
    jj = iiiiiii['test_type'] == 'push'
    iiiiiii_last = iiiiiii.loc[ii&jj]
    iiiiiii_last.drop(columns=['test_type'], inplace=True)
    
    iiiiiii_first.insert(iiiiiii_first.shape[1],'qT_kPa',iiiiiii_first['qT_MPa']*1000)
    iiiiiii_first.insert(iiiiiii_first.shape[1],'Su_ksf',iiiiiii_first['qT_kPa']/iiiiiiiiiii)
    iiiiiii_first['iiiiiiiiiii'] = iiiiiiiiiii
    iiiiiii_last.insert(iiiiiii_last.shape[1],'qT_kPa',iiiiiii_last['qT_MPa']*1000)
    iiiiiii_last.insert(iiiiiii_last.shape[1],'Su_ksf',iiiiiii_last['qT_kPa']/iiiiiiiiiiii)
    iiiiiii_last['iiiiiiiiiiii'] = iiiiiiiiiiii
    
    iiii = pd.concat([iiii,iiiiiii_first])    
    iiiii = pd.concat([iiiii,iiiiiii_last])    
    
'''
## Resulting Tables
#### First push
'''
st.dataframe(iiii)
'''
#### Last push
'''
st.dataframe(iiiii)

def convert_df(df):
     return df.to_csv(index=False).encode('utf-8')

iiiiiiiii = convert_df(iiii)
iiiiiiiiii = convert_df(iiiii)
st.sidebar.markdown('## Download the Processing Results')

st.sidebar.download_button(
     label="Download Tbar_first_push as CSV",
     data=iiiiiiiii,
     file_name='Tbar_first_push.csv',
     mime='text/csv',
 )
#
st.sidebar.download_button(
     label="Download Tbar_last_push as CSV",
     data=iiiiiiiiii,
     file_name='Tbar_last_push.csv',
     mime='text/csv',
 )
