import streamlit as st

import numpy as np
import pandas as pd


add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)

with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)
    

    
