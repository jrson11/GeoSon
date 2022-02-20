import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from pathlib import Path

# Title
st.markdown('## Tangent Lines from log(x)-y plot')

# Sidebar
st.sidebar.markdown('## Tangent Lines: y = ax + b')
#
st.sidebar.markdown('#### Cc')
Cc_point_1_index = st.sidebar.selectbox('Index of starting Cc point', ([0,1,2,3])) 
Cc_point_2_slope = st.sidebar.slider('Slope(a) of ending Cc line', 5.0, 15.0, 10.5)  
Cc_point_2_intercept = st.sidebar.slider('Intercept(b) of ending Cc line', 5.0, 15.0, 10.5) 
#
st.sidebar.markdown('#### Cr')
Cr_point_1_index = st.sidebar.selectbox('Index of starting Cr point', ([0,1,2,3])) 
Cr_point_2_slope = st.sidebar.slider('Slope(a) of ending Cr line', 5.0, 15.0, 10.5)  
Cr_point_2_intercept = st.sidebar.slider('Intercept(b) of ending Cr line', 5.0, 15.0, 10.5)
#
st.sidebar.markdown('#### Cs')
Cs_point_1_index = st.sidebar.selectbox('Index of starting Cs point', ([0,1,2,3])) 
Cs_point_2_slope = st.sidebar.slider('Slope(a) of ending Cs line', 5.0, 15.0, 10.5)  
Cs_point_2_intercept = st.sidebar.slider('Intercept(b) of ending Cs line', 5.0, 15.0, 10.5)

# Data
#df = pd.read_csv('./data-CcCrCs.csv')
#
#st.dataframe(df)
