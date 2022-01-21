import streamlit as st
import numpy as np
import pandas as pd

# -- Create sidebar for plot controls
st.sidebar.markdown('## Set Nt Parameters')
Nt_und = st.sidebar.slider('Nt undisturbed', 5.0, 15.0, 10.5)  # min, max, default
Nt_rem = st.sidebar.slider('Nt remolded', 5.0, 15.0, 10.5)  # min, max, default

# -- Create upbar to import data
asc_list = st.file_uploader("Choose ASC files", accept_multiple_files=True)
n_asc = len(asc_list)

# Processing

def dfTbarfromUniplotASC():
    
    df_TBAR_first = pd.DataFrame()
    df_TBAR_last = pd.DataFrame()
    
    for i in range(n_asc):
        txt_file = asc_list[i]
        loca = txt_file.split()[0]
        print(txt_file)
        


    
