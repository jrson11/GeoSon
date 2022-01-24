import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import streamlit as st

'''
# Geotechnics - Tbar processing
Purpose: To extract the first & last Tbar push data from cycles in Uniplot file \n
Author: J.Son, Ph.D., P.E. \n
Last Update: 1/22/2021 \n
'''

# -- Create sidebar for plot controls
st.sidebar.markdown('## Set Nt Parameters')
Nt_und = st.sidebar.slider('Nt undisturbed', 5.0, 15.0, 10.5)  # min, max, default
Nt_rem = st.sidebar.slider('Nt remolded', 5.0, 15.0, 10.5)  # min, max, default

# -- Create upbar to import data
asc_files = st.sidebar.file_uploader('Choose converted CSV files from Uniplot ASC', accept_multiple_files=True)
n_asc = len(asc_files)
#
'''
## Input files
'''
st.text('Number of ASC files: '+str(n_asc))


# Memory allocation
df_TBAR_first = pd.DataFrame()
df_TBAR_last = pd.DataFrame()

for asc_file in asc_files:
    
    df_asc = pd.read_csv(asc_file, skiprows=41, usecols=[0,1,2,3,4])
    cols = df_asc.columns
    #st.dataframe(df_asc)
    
    # If input file has more header, find 'No'
    ii = df_asc[cols[0]] == 'No'
    #st.dataframe(ii)
    idx = ii[ii].index.astype(int)[0]
    #st.text(idx)
    df_tbar = df_asc.loc[idx+1:,cols[0:5]]
    df_tbar.columns = ['Rec','Depth_m','Time_s','qT','qT_pull']
        
    # Reset index
    df_tbar.reset_index(inplace=True)
    df_tbar.drop(columns='index', inplace=True)    
    #st.dataframe(df_tbar)
    
    #
    iiii.loc[:,'Rec'] = pd.to_numeric(iiii.loc[:,'Rec'])
    iiii.loc[:,'Depth_m'] = pd.to_numeric(iiii.loc[:,'Depth_m'])
    iiii.loc[:,'Time_s'] = pd.to_numeric(iiii.loc[:,'Time_s'])
    iiii.loc[:,'qT'] = pd.to_numeric(iiii.loc[:,'qT'])
    iiii.loc[:,'qT_pull'] = pd.to_numeric(iiii.loc[:,'qT_pull'])
    #st.dataframe(iiii)
    #
    iiii['qT_MPa'] = np.nan
    ii = iiii['qT'].isnull()
    #st.dataframe(ii)
    iiii.loc[~ii,'qT_MPa'] = iiii.loc[~ii,'qT']
    ii = iiii['qT_pull'].isnull()
    #st.dataframe(ii)
    iiii.loc[~ii,'qT_MPa'] = iiii.loc[~ii,'qT_pull']
    iiii.drop(columns=['qT','qT_pull'], inplace=True)
    
    if iiii.loc[0,'qT_MPa'] < 0:
        iiii.loc[0,'qT_MPa'] = 0
    
    # Define push & pull to find cycles
    iiii['test_type'] = 'push'
    ii = iiii.loc[:,'qT_MPa'] < 0
    iiii.loc[ii,'test_type'] = 'pull'
    #
    iiii['diff'] = (iiii.test_type != iiii.test_type.shift()).astype(int)
    iiii['diff_cumsum'] = iiii['diff'].cumsum()
    iiii['cycle'] = np.floor((iiii['diff_cumsum']-1)/2+1).astype(int)    
    iiii.drop(columns=['diff','diff_cumsum'], inplace=True)
    st.dataframe(iiii)
    # Add location
    loca = asc_file.name.split()[0]
    st.text(loca)
    iiii.insert(0,'Loca',loca)
    
    # Fine first and last push only
    ii = iiii['cycle'] == 1
    jj = iiii['test_type'] == 'push'
    df_tbar_first = iiii.loc[ii&jj]
    df_tbar_first.drop(columns=['test_type'], inplace=True)
    #
    ii = iiii['cycle'] == max(iiii['cycle'])
    jj = iiii['test_type'] == 'push'
    df_tbar_last = iiii.loc[ii&jj]
    df_tbar_last.drop(columns=['test_type'], inplace=True)
    
    # Calculate Su
    iiiii.insert(iiiii.shape[1],'qT_kPa',iiiii['qT_MPa']*1000)
    iiiii.insert(iiiii.shape[1],'Su_ksf',iiiii['qT_kPa']/Nt_und)
    iiiii['Nt_und'] = Nt_und
    iiiiii.insert(iiiiii.shape[1],'qT_kPa',iiiiii['qT_MPa']*1000)
    iiiiii.insert(iiiiii.shape[1],'Su_ksf',iiiiii['qT_kPa']/Nt_rem)
    iiiiii['Nt_rem'] = Nt_rem
    
    # Combine all
    df_TBAR_first = pd.concat([df_TBAR_first,iiiii])    
    df_TBAR_last = pd.concat([df_TBAR_last,iiiiii])    
    
        
## -- Plotting
locas = np.unique(df_TBAR_first['Loca'])
zmax = max(df_TBAR_first['Depth_m'])




## -- Table
'''
## Resulting Tables
#### First push
'''
st.dataframe(df_TBAR_first)
'''
#### Last push
'''
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
