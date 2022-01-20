import streamlit as st

import numpy as np
import pandas as pd



# -- Create sidebar for plot controls
st.sidebar.markdown('## Set Plot Parameters')
Nt_und = st.sidebar.slider('Nt undisturbed', 0.1, 8.0, 1.0)  # min, max, default



# -- Create upbar to import data
uploaded_files = st.file_uploader("Choose ASC files", accept_multiple_files=True)


with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)
    
