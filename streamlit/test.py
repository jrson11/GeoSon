import streamlit as st
import streamlit.components.v1 as components

st.markdown('## Hi')


st.header("test html import")

HtmlFile = open("google.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
print(source_code)
components.html(source_code, height = 600)
