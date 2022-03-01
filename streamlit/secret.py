import streamlit as st

st.markdown("# Test page to keep secret")

password = st.sidebar.text_input('Password?', 'password')

if password == st.secrets["db_password"]:
  st.write('Welcome to KUPEA')
  main()
  
else:
  st.write('Please join KUPEA')


def main():
  st.write('Assa')
