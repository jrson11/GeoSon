import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import streamlit as st

'''
# Geotechnics - Tbar processing
Purpose: To extract the first & last Tbar push data from cycles in Uniplot file \n
Author: J.Son, Ph.D., P.E. \n
Last Update: 1/22/2021 \n
Note: I am so sorry for my bad coding script \n
'''

st.sidebar.markdown('## Set Nt Parameters')
Nt_und = st.sidebar.slider('Nt undisturbed', 5.0, 15.0, 10.5)  # min, max, default
Nt_rem = st.sidebar.slider('Nt remolded', 5.0, 15.0, 10.5)  # min, max, default
asc_files = st.sidebar.file_uploader('Choose converted CSV files from Uniplot ASC', accept_multiple_files=True)
n_asc = len(asc_files)
#
'''
## Input files
'''
st.text('Number of ASC files: '+str(n_asc))

# Memory allocation
iiiiii = pd.DataFrame()
iiiiiii = pd.DataFrame()

for asc_file in asc_files:
    
    iiiiiiii = pd.read_csv(asc_file, skiprows=41, usecols=[0,1,2,3,4])
    cols = iiiiiiii.columns
    #
    ii = iiiiiiii[cols[0]] == 'No'
    idx = ii[ii].index.astype(int)[0]
    iiiiiiiiiiii = iiiiiiii.loc[idx+1:,cols[0:5]]
    iiiiiiiiiiii.columns = ['Rec','Depth_m','Time_s','qT','qT_pull']
    #    
    iiiiiiiiiiii.reset_index(inplace=True)
    iiiiiiiiiiii.drop(columns='index', inplace=True)    
    #
    iiiiiiiiiiii.loc[:,'Rec'] = pd.to_numeric(iiiiiiiiiiii.loc[:,'Rec'])
    iiiiiiiiiiii.loc[:,'Depth_m'] = pd.to_numeric(iiiiiiiiiiii.loc[:,'Depth_m'])
    iiiiiiiiiiii.loc[:,'Time_s'] = pd.to_numeric(iiiiiiiiiiii.loc[:,'Time_s'])
    iiiiiiiiiiii.loc[:,'qT'] = pd.to_numeric(iiiiiiiiiiii.loc[:,'qT'])
    iiiiiiiiiiii.loc[:,'qT_pull'] = pd.to_numeric(iiiiiiiiiiii.loc[:,'qT_pull'])
    #
    iiiiiiiiiiii['qT_MPa'] = np.nan
    ii = iiiiiiiiiiii['qT'].isnull()
    iiiiiiiiiiii.loc[~ii,'qT_MPa'] = iiiiiiiiiiii.loc[~ii,'qT']
    ii = iiiiiiiiiiii['qT_pull'].isnull()
    iiiiiiiiiiii.loc[~ii,'qT_MPa'] = iiiiiiiiiiii.loc[~ii,'qT_pull']
    iiiiiiiiiiii.drop(columns=['qT','qT_pull'], inplace=True)
    
    if iiiiiiiiiiii.loc[0,'qT_MPa'] < 0:
        iiiiiiiiiiii.loc[0,'qT_MPa'] = 0
    
    iiiiiiiiiiii['test_type'] = 'push'
    ii = iiiiiiiiiiii.loc[:,'qT_MPa'] < 0
    iiiiiiiiiiii.loc[ii,'test_type'] = 'pull'
    #
    iiiiiiiiiiii['diff'] = (iiiiiiiiiiii.test_type != iiiiiiiiiiii.test_type.shift()).astype(int)
    iiiiiiiiiiii['diff_cumsum'] = iiiiiiiiiiii['diff'].cumsum()
    iiiiiiiiiiii['cycle'] = np.floor((iiiiiiiiiiii['diff_cumsum']-1)/2+1).astype(int)    
    iiiiiiiiiiii.drop(columns=['diff','diff_cumsum'], inplace=True)
    st.dataframe(iiiiiiiiiiii)
    loca = asc_file.name.split()[0]
    st.text(loca)
    iiiiiiiiiiii.insert(0,'Loca',loca)
    
    ii = iiiiiiiiiiii['cycle'] == 1
    jj = iiiiiiiiiiii['test_type'] == 'push'
    iiii = iiiiiiiiiiii.loc[ii&jj]
    iiii.drop(columns=['test_type'], inplace=True)
    #
    ii = iiiiiiiiiiii['cycle'] == max(iiiiiiiiiiii['cycle'])
    jj = iiiiiiiiiiii['test_type'] == 'push'
    iiiii = iiiiiiiiiiii.loc[ii&jj]
    iiiii.drop(columns=['test_type'], inplace=True)
    
    iiii.insert(iiii.shape[1],'qT_kPa',iiii['qT_MPa']*1000)
    iiii.insert(iiii.shape[1],'Su_ksf',iiii['qT_kPa']/Nt_und)
    iiii['Nt_und'] = Nt_und
    iiiii.insert(iiiii.shape[1],'qT_kPa',iiiii['qT_MPa']*1000)
    iiiii.insert(iiiii.shape[1],'Su_ksf',iiiii['qT_kPa']/Nt_rem)
    iiiii['Nt_rem'] = Nt_rem
    
    iiiiii = pd.concat([iiiiii,iiii])    
    iiiiiii = pd.concat([iiiiiii,iiiii])    

'''
## Resulting Tables
#### First push
'''
st.dataframe(iiiiii)
'''
#### Last push
'''
st.dataframe(iiiiiii)

def convert_df(df):
     return df.to_csv(index=False).encode('utf-8')

csv_first = convert_df(iiiiii)
csv_last = convert_df(iiiiiii)

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
