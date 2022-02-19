import numpy as np
import pandas as pd
import streamlit as st

# Title
st.markdown('## ez_Cc Cr Cs from log(x)-y plot')

# Sidebar
st.sidebar.markdown('## Tangent Lines')
Cc_point_1_index = st.sidebar.slider('Nt undisturbed', 5.0, 15.0, 10.5)  # min, max, default
Cc_point_2_slope = st.sidebar.slider('Nt undisturbed', 5.0, 15.0, 10.5)  # min, max, default
Cc_point_2_intercept = st.sidebar.slider('Nt undisturbed', 5.0, 15.0, 10.5)  # min, max, default
#
Cr_point_1_index = st.sidebar.slider('Nt undisturbed', 5.0, 15.0, 10.5)  # min, max, default
Cr_point_2_slope = st.sidebar.slider('Nt undisturbed', 5.0, 15.0, 10.5)  # min, max, default
Cr_point_2_intercept = st.sidebar.slider('Nt undisturbed', 5.0, 15.0, 10.5)  # min, max, default
#
Cs_point_1_index = st.sidebar.slider('Nt undisturbed', 5.0, 15.0, 10.5)  # min, max, default
Cs_point_2_slope = st.sidebar.slider('Nt undisturbed', 5.0, 15.0, 10.5)  # min, max, default
Cs_point_2_intercept = st.sidebar.slider('Nt undisturbed', 5.0, 15.0, 10.5)  # min, max, default

x = np.linspace(1,10,1)
y = x*2

st.dataframe(pd.DataFrame(y))
