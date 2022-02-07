import streamlit as st
import streamlit.components.v1 as components

st.markdown('## Hi')


st.header("test html import")

HtmlFile = open("https://github.com/jrson11/GeoSon/blob/main/streamlit/google.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
print(source_code)
components.html(source_code)
