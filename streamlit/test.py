import streamlit as st

import numpy as np
import pandas as pd
import altair as alt
from vega_datasets import data


with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)
    
    counties = alt.topo_feature(data.us_10m.url, 'counties')
    source = data.unemployment.url
    
    st.altair_chart(alt.Chart(counties)
        .mark_geoshape()
        .encode(color='rate:Q')
        .transform_lookup(lookup='id',from_=alt.LookupData(source, 'id', ['rate']))
        .project(type='albersUsa')
        .properties(width=500,height=300))
