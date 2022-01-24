import numpy as np
import pandas as pd
import streamlit as st

'''
# Geotechnics - Tbar processing
Purpose: To extract the first & last Tbar push data from cycles in Uniplot file \n
Author: J.Son, Ph.D., P.E. \n
Last Update: 1/22/2021 \n
'''

# Create sidebar for plot controls
st.sidebar.markdown('## Set Nt Parameters')
Nt_und = st.sidebar.slider('Nt undisturbed', 5.0, 15.0, 10.5)  # min, max, default
Nt_rem = st.sidebar.slider('Nt remolded', 5.0, 15.0, 10.5)  # min, max, default

# Create upbar to import data
iiiiiiiiii = st.sidebar.file_uploader('Choose converted CSV files from Uniplot ASC', accept_multiple_files=True)
iiiiiiiiiii = len(iiiiiiiiii)
#
'''
## Input files
'''
st.text('Number of imported CSV files: '+str(iiiiiiiiiii))

def dfTbarfromUniplotCSV(Nt_und,Nt_rem):
    return 0

# Memory allocation
iii = pd.DataFrame()
iiii = pd.DataFrame()

# Processing
for iiiiiiiiiiii in iiiiiiiiii:
    
    iiiii = pd.read_csv(iiiiiiiiiiii, skiprows=60)
    cols = iiiii.columns
    
    ii = iiiii[cols[0]] == 'No'
    idx = ii[ii].index.astype(int)[0]
    iiiiii = iiiii.loc[idx+1:,cols[0:5]]
    iiiiii.columns = ['Rec','Depth_m','Time_s','qT','qT_pull']
        
    iiiiii.reset_index(inplace=True)
    iiiiii.drop(columns='index', inplace=True)    
    
    iiiiii.loc[:,'Rec'] = pd.to_numeric(iiiiii.loc[:,'Rec'])
    iiiiii.loc[:,'Depth_m'] = pd.to_numeric(iiiiii.loc[:,'Depth_m'])
    iiiiii.loc[:,'Time_s'] = pd.to_numeric(iiiiii.loc[:,'Time_s'])
    iiiiii.loc[:,'qT'] = pd.to_numeric(iiiiii.loc[:,'qT'])
    iiiiii.loc[:,'qT_pull'] = pd.to_numeric(iiiiii.loc[:,'qT_pull'])
    #
    iiiiii['qT_MPa'] = np.nan
    ii = iiiiii['qT'].isnull()
    iiiiii.loc[~ii,'qT_MPa'] = iiiiii.loc[~ii,'qT']
    ii = iiiiii['qT_pull'].isnull()
    iiiiii.loc[~ii,'qT_MPa'] = iiiiii.loc[~ii,'qT_pull']
    iiiiii.drop(columns=['qT','qT_pull'], inplace=True)
    
    iiiiii['test_type'] = 'push'
    ii = iiiiii.loc[:,'qT_MPa'] < 0
    iiiiii.loc[ii,'test_type'] = 'pull'
    #
    iiiiii['diff'] = (iiiiii.test_type != iiiiii.test_type.shift()).astype(int)
    iiiiii['diff_cumsum'] = iiiiii['diff'].cumsum()
    iiiiii['cycle'] = np.floor((iiiiii['diff_cumsum']-1)/2+1).astype(int)    
    iiiiii.drop(columns=['diff','diff_cumsum'], inplace=True)
    
    iiiiiii = iiiiiiiiiiii.name.split()[0]
    st.text(iiiiiii)
    iiiiii.insert(0,'Loca',iiiiiii)
    
    ii = iiiiii['cycle'] == 1
    jj = iiiiii['test_type'] == 'push'
    iiiiii_first = iiiiii.loc[ii&jj]
    iiiiii_first.drop(columns=['test_type'], inplace=True)
    #
    ii = iiiiii['cycle'] == max(iiiiii['cycle'])
    jj = iiiiii['test_type'] == 'push'
    iiiiii_last = iiiiii.loc[ii&jj]
    iiiiii_last.drop(columns=['test_type'], inplace=True)
    
    iiiiii_first.insert(iiiiii_first.shape[1],'qT_kPa',iiiiii_first['qT_MPa']*1000)
    iiiiii_first.insert(iiiiii_first.shape[1],'Su_ksf',iiiiii_first['qT_kPa']/Nt_und)
    iiiiii_first['Nt_und'] = Nt_und
    iiiiii_last.insert(iiiiii_last.shape[1],'qT_kPa',iiiiii_last['qT_MPa']*1000)
    iiiiii_last.insert(iiiiii_last.shape[1],'Su_ksf',iiiiii_last['qT_kPa']/Nt_rem)
    iiiiii_last['Nt_rem'] = Nt_rem
    
    iii = pd.concat([iii,iiiiii_first])    
    iiii = pd.concat([iiii,iiiiii_last])    
    
        

'''
## Resulting Tables

#### First Push
'''
st.dataframe(iii)
'''
#### Last Push
'''
st.dataframe(iiii)

def convert_df(df):
     return df.to_csv(index=False).encode('utf-8')

iiiiiiii = convert_df(iii)
iiiiiiiii = convert_df(iiii)

st.sidebar.markdown('## Download the Processing Results')

st.sidebar.download_button(
     label="Download Tbar_first_push as CSV",
     data=iiiiiiii,
     file_name='Tbar_first_push.csv',
     mime='text/csv',
 )
#
st.sidebar.download_button(
     label="Download Tbar_last_push as CSV",
     data=iiiiiiiii,
     file_name='Tbar_last_push.csv',
     mime='text/csv',
 )
