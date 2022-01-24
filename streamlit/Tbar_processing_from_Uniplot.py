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
    df_tbar.loc[:,'Rec'] = pd.to_numeric(df_tbar.loc[:,'Rec'])
    df_tbar.loc[:,'Depth_m'] = pd.to_numeric(df_tbar.loc[:,'Depth_m'])
    df_tbar.loc[:,'Time_s'] = pd.to_numeric(df_tbar.loc[:,'Time_s'])
    df_tbar.loc[:,'qT'] = pd.to_numeric(df_tbar.loc[:,'qT'])
    df_tbar.loc[:,'qT_pull'] = pd.to_numeric(df_tbar.loc[:,'qT_pull'])
    #st.dataframe(df_tbar)
    #
    df_tbar['qT_MPa'] = np.nan
    ii = df_tbar['qT'].isnull()
    #st.dataframe(ii)
    df_tbar.loc[~ii,'qT_MPa'] = df_tbar.loc[~ii,'qT']
    ii = df_tbar['qT_pull'].isnull()
    #st.dataframe(ii)
    df_tbar.loc[~ii,'qT_MPa'] = df_tbar.loc[~ii,'qT_pull']
    df_tbar.drop(columns=['qT','qT_pull'], inplace=True)
    
    if df_tbar.loc[0,'qT_MPa'] < 0:
        df_tbar.loc[0,'qT_MPa'] = 0
    
    # Define push & pull to find cycles
    df_tbar['test_type'] = 'push'
    ii = df_tbar.loc[:,'qT_MPa'] < 0
    df_tbar.loc[ii,'test_type'] = 'pull'
    #
    df_tbar['diff'] = (df_tbar.test_type != df_tbar.test_type.shift()).astype(int)
    df_tbar['diff_cumsum'] = df_tbar['diff'].cumsum()
    df_tbar['cycle'] = np.floor((df_tbar['diff_cumsum']-1)/2+1).astype(int)    
    df_tbar.drop(columns=['diff','diff_cumsum'], inplace=True)
    st.dataframe(df_tbar)
    # Add location
    loca = asc_file.name.split()[0]
    st.text(loca)
    df_tbar.insert(0,'Loca',loca)
    
    # Fine first and last push only
    ii = df_tbar['cycle'] == 1
    jj = df_tbar['test_type'] == 'push'
    iiii = df_tbar.loc[ii&jj]
    iiii.drop(columns=['test_type'], inplace=True)
    #
    ii = df_tbar['cycle'] == max(df_tbar['cycle'])
    jj = df_tbar['test_type'] == 'push'
    df_tbar_last = df_tbar.loc[ii&jj]
    df_tbar_last.drop(columns=['test_type'], inplace=True)
    
    # Calculate Su
    iiii.insert(iiii.shape[1],'qT_kPa',iiii['qT_MPa']*1000)
    iiii.insert(iiii.shape[1],'Su_ksf',iiii['qT_kPa']/Nt_und)
    iiii['Nt_und'] = Nt_und
    df_tbar_last.insert(df_tbar_last.shape[1],'qT_kPa',df_tbar_last['qT_MPa']*1000)
    df_tbar_last.insert(df_tbar_last.shape[1],'Su_ksf',df_tbar_last['qT_kPa']/Nt_rem)
    df_tbar_last['Nt_rem'] = Nt_rem
    
    # Combine all
    iiii = pd.concat([iiii,iiii])    
    df_TBAR_last = pd.concat([df_TBAR_last,df_tbar_last])    
    
        
## -- Plotting
locas = np.unique(iiii['Loca'])
zmax = max(iiii['Depth_m'])

def matplot_Tbar(locas,zmax):

    fig,ax = plt.subplots(1,2, figsize=(9,7), dpi=300)

    for i in range(len(locas)):
        loca = locas[i]
        ii = iiii['Loca'] == loca
        jj = df_TBAR_last['Loca'] == loca
        #
        ax[0].plot(iiii.loc[ii,'Su_ksf'],iiii.loc[ii,'Depth_m'],'.',alpha=0.5,label=loca)
        ax[0].set_xlabel('Su [ksf]')
        ax[0].set_ylabel('Depth [m]')
        ax[0].set_title('Tbar first push')
        #
        ax[1].plot(df_TBAR_last.loc[jj,'Su_ksf'],df_TBAR_last.loc[jj,'Depth_m'],'.',alpha=0.5,label=loca)
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
st.dataframe(iiii)
'''
#### Last push
'''
st.dataframe(df_TBAR_last)




def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv(index=False).encode('utf-8')


csv_first = convert_df(iiii)
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
