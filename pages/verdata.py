
import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page


#----newurl = 'https://raw.githubusercontent.com/pjluispb/miscvs/main/Prondanmin23.csv'
newurl = pd.read_csv("Prondanmin23.csv", index_col='cedula')
#st.write(newurl.head(5))


with st.expander('ver data'):
    newurl
regresar = st.button('Volver')
if regresar:
    switch_page('logmi')

#busq = pdwks.where(pdwks['Cédula de Identidad']='5125570')
#busq = pdwks[pdwks['Cédula de Identidad'].str.contains('5125570')]
#fibusq