import streamlit as st

st.markdown('# Test page to keep secret')

username = st.sidebar.text_input('Username', 'username')
password = st.sidebar.text_input('Password', 'password')


st.write('The current movie title is', title)

st.write("DB username:", st.secrets["db_username"])
st.write("DB password:", st.secrets["db_password"])


