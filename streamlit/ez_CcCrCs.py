import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

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
x = [1.03,1.04,1.03,1.26,1.27,1.38,1.47,1.52,1.63,1.76,1.84,1.94,2.08,2.21,2.37,2.52,2.68,2.83,2.99,3.18,3.37,3.55,3.76,3.97,4.21,4.45,4.71,4.99,5.27,5.57,5.89,6.21,6.56,6.92,7.27,7.66,8.05,8.45,8.51,8.55,8.85,8.84,8.86,8.85,8.85,8.23,6.9,5.97,5.86,5.17,4.6,4.1,3.68,3.32,2.99,2.7,2.45,2.22,2.02,1.83,1.68,1.53,1.36,1.24,1.13,1.06,1.05,1.01,0.91,0.9,0.91,0.91,0.9,1.05,2.45,3.93,5.75,8.07,10.77,13.73,17.01,20.7,24.93,29.63,34.81,40.47,46.57,53.26,60.29,67.92,76.12,84.7,93.88,103.61,113.79,123.96,135.05,146.99,159.17,171.9,184.73,198.36,211.99,226.66,241.11,241.11,241.32,242.07,242.15,242.18,242.17,242.17,241.55,218.32,195.99,175.45,156.14,139.13,123.41,109.2,95.84,84.67,73.69,64.01,55.35,47.73,41.08,35.26,30.45,25.99,22.08,18.79,15.92,15.08]
y = [0.749,0.75,0.75,0.751,0.75,0.748,0.747,0.746,0.743,0.741,0.741,0.74,0.737,0.734,0.733,0.731,0.73,0.728,0.725,0.724,0.723,0.72,0.718,0.716,0.714,0.711,0.71,0.708,0.705,0.704,0.703,0.7,0.699,0.696,0.694,0.693,0.691,0.689,0.688,0.688,0.685,0.685,0.684,0.684,0.684,0.684,0.685,0.687,0.687,0.689,0.691,0.693,0.695,0.698,0.699,0.702,0.704,0.705,0.706,0.709,0.712,0.713,0.717,0.719,0.721,0.723,0.723,0.724,0.727,0.727,0.727,0.728,0.728,0.728,0.719,0.708,0.698,0.687,0.679,0.669,0.659,0.65,0.64,0.632,0.622,0.612,0.602,0.594,0.585,0.575,0.567,0.557,0.549,0.54,0.531,0.524,0.516,0.508,0.5,0.493,0.484,0.478,0.469,0.464,0.456,0.455,0.456,0.454,0.454,0.453,0.453,0.452,0.452,0.451,0.453,0.453,0.456,0.459,0.462,0.465,0.469,0.473,0.476,0.482,0.487,0.493,0.499,0.505,0.511,0.517,0.524,0.531,0.539,0.542]
#
df = pd.DataFrame()
df['X'] = x
df['Y'] = y
df.insert(0,'NAME','BH_A00')

#
st.text(str(nx))
st.text(str(ny))

st.dataframe(df)


fig = alt.Chart(df).mark_point.encode(
  x = alt.X('X'),
  y = alt.Y('Y')
  ).properties(title='X-Y plot', width=200, height=400
  )
#
st.altair_chart(fig)
