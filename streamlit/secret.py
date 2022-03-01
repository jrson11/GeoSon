import streamlit as st

st.markdown("# Test page to keep secret")

password = st.sidebar.text_input('Password?', 'password')

if password == st.secrets["db_password"]:
  st.markdown('## Welcome to KUPEA')
  main()
  
else:
  st.markdown('## Please join KUPEA')


def main():
  st.write('Assa')
