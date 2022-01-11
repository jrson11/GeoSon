import numpy as np
import pandas as pd
import streamlit as st

with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)
    
    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns
