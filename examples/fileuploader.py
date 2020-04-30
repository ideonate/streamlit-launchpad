import streamlit as st
import glob
from os import path
import pandas as pd

st.markdown('# Based on subfolder path')

path_input_data = st.sidebar.text_input("Provide the name to the subfolder in which your csv files are "

                                            "stored.")
st.write("Input path:", path_input_data)

docker_search_path = path.join('.', path_input_data)

st.write("Search path:", docker_search_path)

if path_input_data:

    excel_files = glob.glob(docker_search_path + '/**/*.csv', recursive=True)

    st.write(excel_files)



st.markdown('# Now try uploading')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:

     st.write('Uploaded file: ', uploaded_file)
     data = pd.read_csv(uploaded_file)
     st.write(data)


st.write('Streamlit version: ', st.version._get_installed_streamlit_version())