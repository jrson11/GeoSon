import streamlit as st

st.markdown("# Test page to keep secret")

password = st.sidebar.text_input('Password', 'password')

if password == st.secrets["db_password"]:
  st.write('Welcome to KUPEA')
  
else:
  st.write('Please join KUPEA')

st.write("DB username:", st.secrets["db_username"])
st.write("DB password:", st.secrets["db_password"])


