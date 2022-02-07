import pandas as pd
import streamlit as st

st.markdown('## To combine multiple Excel files into one file')

st.sidebar.markdown('## Input')
t_data = st.sidebar.selectbox('Type of input data file',['xlsx','xls','csv'])

if t_data == 'xlsx':
    iii = st.sidebar.file_uploader('Choose input files',type=['xlsx'], accept_multiple_files=True)
elif t_data == 'xls':
    iii = st.sidebar.file_uploader('Choose input files',type=['xls'], accept_multiple_files=True)
elif t_data == 'csv':
    iii = st.sidebar.file_uploader('Choose input files',type=['csv'], accept_multiple_files=True)

n_input = len(iii)
st.markdown('#### Input files')
st.text('Number of uploaded files: '+str(n_input))

iiiiii = st.sidebar.selectbox('Number of header lines to skip',[0,1,2,3,4,5,6,7,8,9,10])

iiiii = pd.DataFrame()
for input_file in iii:
    st.text(input_file.name)
    iiii = pd.read_excel(input_file, header=iiiiii)
    iiii.insert(0,'File',input_file.name)
    iiiii = pd.concat([iiiii,iiii.loc[1:,:]])    

st.markdown('#### Output result')
st.dataframe(iiiii)

def convert_df(df):
     return df.to_csv(index=False).encode('utf-8')

csv_result = convert_df(iiiii)

st.sidebar.markdown('## Output')

st.sidebar.download_button(
     label="Download result table",
     data=csv_result,
     file_name='all_data.csv',
     mime='text/csv',
 )

