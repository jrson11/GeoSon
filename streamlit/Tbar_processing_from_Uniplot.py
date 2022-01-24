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
III1 = pd.DataFrame()
III0 = pd.DataFrame()

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
    iii.loc[:,'Rec'] = pd.to_numeric(iii.loc[:,'Rec'])
    iii.loc[:,'Depth_m'] = pd.to_numeric(iii.loc[:,'Depth_m'])
    iii.loc[:,'Time_s'] = pd.to_numeric(iii.loc[:,'Time_s'])
    iii.loc[:,'qT'] = pd.to_numeric(iii.loc[:,'qT'])
    iii.loc[:,'qT_pull'] = pd.to_numeric(iii.loc[:,'qT_pull'])
    #st.dataframe(iii)
    #
    iii['qT_MPa'] = np.nan
    ii = iii['qT'].isnull()
    #st.dataframe(ii)
    iii.loc[~ii,'qT_MPa'] = iii.loc[~ii,'qT']
    ii = iii['qT_pull'].isnull()
    #st.dataframe(ii)
    iii.loc[~ii,'qT_MPa'] = iii.loc[~ii,'qT_pull']
    iii.drop(columns=['qT','qT_pull'], inplace=True)
    
    if iii.loc[0,'qT_MPa'] < 0:
        iii.loc[0,'qT_MPa'] = 0
    
    # Define push & pull to find cycles
    iii['test_type'] = 'push'
    ii = iii.loc[:,'qT_MPa'] < 0
    iii.loc[ii,'test_type'] = 'pull'
    #
    iii['diff'] = (iii.test_type != iii.test_type.shift()).astype(int)
    iii['diff_cumsum'] = iii['diff'].cumsum()
    iii['cycle'] = np.floor((iii['diff_cumsum']-1)/2+1).astype(int)    
    iii.drop(columns=['diff','diff_cumsum'], inplace=True)
    st.dataframe(iii)
    # Add location
    loca = asc_file.name.split()[0]
    st.text(loca)
    iii.insert(0,'Loca',loca)
    
    # Fine first and last push only
    ii = iii['cycle'] == 1
    jj = iii['test_type'] == 'push'
    df_tbar_first = iii.loc[ii&jj]
    df_tbar_first.drop(columns=['test_type'], inplace=True)
    #
    ii = iii['cycle'] == max(iii['cycle'])
    jj = iii['test_type'] == 'push'
    df_tbar_last = iii.loc[ii&jj]
    df_tbar_last.drop(columns=['test_type'], inplace=True)
    
    # Calculate Su
    df_tbar_first.insert(df_tbar_first.shape[1],'qT_kPa',df_tbar_first['qT_MPa']*1000)
    df_tbar_first.insert(df_tbar_first.shape[1],'Su_ksf',df_tbar_first['qT_kPa']/Nt_und)
    df_tbar_first['Nt_und'] = Nt_und
    df_tbar_last.insert(df_tbar_last.shape[1],'qT_kPa',df_tbar_last['qT_MPa']*1000)
    df_tbar_last.insert(df_tbar_last.shape[1],'Su_ksf',df_tbar_last['qT_kPa']/Nt_rem)
    df_tbar_last['Nt_rem'] = Nt_rem
    
    # Combine all
    III1 = pd.concat([III1,df_tbar_first])    
    III0 = pd.concat([III0,df_tbar_last])    
    
        
## -- Plotting
locas = np.unique(III1['Loca'])
zmax = max(III1['Depth_m'])

def matplot_Tbar(locas,zmax):

    fig,ax = plt.subplots(1,2, figsize=(9,7), dpi=300)

    for i in range(len(locas)):
        loca = locas[i]
        ii = III1['Loca'] == loca
        jj = III0['Loca'] == loca
        #
        ax[0].plot(III1.loc[ii,'Su_ksf'],III1.loc[ii,'Depth_m'],'.',alpha=0.5,label=loca)
        ax[0].set_xlabel('Su [ksf]')
        ax[0].set_ylabel('Depth [m]')
        ax[0].set_title('Tbar first push')
        #
        ax[1].plot(III0.loc[jj,'Su_ksf'],III0.loc[jj,'Depth_m'],'.',alpha=0.5,label=loca)
        ax[1].set_xlabel('Su [ksf]')
        ax[1].set_title('Tbar last push')
        #
        for k in range(2):
            ax[k].set(ylim=(zmax+1,0))
            ax[k].legend(loc='upper center', bbox_to_anchor=(0.5, 0), fancybox=True, shadow=False)
            ax[k].grid(linestyle='dotted')
            ax[k].minorticks_on()
            ax[k].xaxis.set_ticks_position('top')
            ax[k].xaxis.set_label_position('top')
            ax[k].yaxis.grid(which="minor",linestyle='dotted')    
        
    st.pyplot(fig)
    
#matplot_Tbar(locas,zmax)



## -- Table
'''
## Resulting Tables
#### First push
'''
st.dataframe(III1)
'''
#### Last push
'''
st.dataframe(III0)




def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv(index=False).encode('utf-8')


csv_first = convert_df(III1)
csv_last = convert_df(III0)

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
