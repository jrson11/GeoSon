import streamlit as st

# Initialization ----------------------------------------
st.markdown("# Test page to keep secret")
password = st.sidebar.text_input('Password?', 'password')

# Main --------------------------------------------------
def main():
  st.write('Assa')

# Membership --------------------------------------------
if password == st.secrets["db_password"]:
  st.markdown('## Welcome to KUPEA')
  main()
  
else:
  st.markdown('## Please join KUPEA')



