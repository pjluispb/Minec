
import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page


urlcsv = 'https://raw.githubusercontent.com/pjluispb/miscvs/main/Prondanmin23.csv'
newurl = pd.read_csv(urlcsv, index_col='cedula')


with st.expander('ver data'):
    newurl
regresar = st.button('Volver')
if regresar:
    switch_page('logmi')
