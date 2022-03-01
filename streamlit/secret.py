import streamlit as st


title = st.sidebar.text_input('Movie title', 'Life of Brian')
st.write('The current movie title is', title)

#st.write("DB username:", st.secrets["db_username"])

