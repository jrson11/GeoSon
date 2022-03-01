import streamlit as st

st.markdown("# Test page to keep secret")

password = st.sidebar.text_input('Password', 'password')


st.write("DB username:", st.secrets["db_username"])
st.write("DB password:", st.secrets["db_password"])


