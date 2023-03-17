import pygsheets
import pandas as pd
from deta import Deta
import random
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import time

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')


deta = Deta(st.secrets["deta_key"])
SCOPES = ('https://www.spreadshhets.com/feeds', 'https://www.googleapis.com/auth/drive')
credentials = st.secrets["gcp_service_account"]
#gc = pygsheets.authorize(custom_credentials=credentials)
gc = pygsheets.authorize()
accesos = deta.Base('minec-accesos')
res=accesos.fetch()
   
st.write('gc = ',gc)
st.write('deta = ',deta)
try:
   gsheetsTit = gc.spreadsheet_titles()       #obtiene la lista de todas las gsheets
except:
   st.write('No funciona gc.spreadsheet_titles()')
try:
   gsheet1 = gc.open('M2uno')
   st.write('abierto M2uno')
   st.write(gsheet1)
except:
   st.write('falla abriendo M2uno')
#files = [x for x in gsheetsTit if x.startswith('M2')]    #obtiene la lista de los gsheets que comienzan con M2
