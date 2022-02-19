import numpy as np
import pandas as pd
import streamlit as st

# Title
st.markdown('## ez_Cc Cr Cs from log(x)-y plot')

# Sidebar
st.sidebar.markdown('## Tangent Lines: y = ax + b')
Cc_point_1_index = st.sidebar.slider('Index of starting Cc point', 5.0, 15.0, 10.5) 
Cc_point_2_slope = st.sidebar.slider('Slope(a) of ending Cc line', 5.0, 15.0, 10.5)  
Cc_point_2_intercept = st.sidebar.slider('Intercept(b) of ending Cc line', 5.0, 15.0, 10.5) 
#
Cr_point_1_index = st.sidebar.slider('Index of starting Cr point', 5.0, 15.0, 10.5) 
Cr_point_2_slope = st.sidebar.slider('Slope(a) of ending Cr line', 5.0, 15.0, 10.5)  
Cr_point_2_intercept = st.sidebar.slider('Intercept(b) of ending Cr line', 5.0, 15.0, 10.5)
#
Cs_point_1_index = st.sidebar.slider('Index of starting Cs point', 5.0, 15.0, 10.5) 
Cs_point_2_slope = st.sidebar.slider('Slope(a) of ending Cs line', 5.0, 15.0, 10.5)  
Cs_point_2_intercept = st.sidebar.slider('Intercept(b) of ending Cs line', 5.0, 15.0, 10.5)

x = np.linspace(1,10,1)
y = x*2

st.dataframe(pd.DataFrame(y))
