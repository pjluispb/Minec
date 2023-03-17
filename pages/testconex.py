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
credentials = st.secrets["gcp_service_account"]
gc = pygsheets.authorize(custom_credentials=credentials)
accesos = deta.Base('minec-accesos')
res=accesos.fetch()
   
st.write('gc = ',gc)
st.write('deta = ',deta)
#gsheetsTit = gc.spreadsheet_titles()       #obtiene la lista de todas las gsheets
#files = [x for x in gsheetsTit if x.startswith('M2')]    #obtiene la lista de los gsheets que comienzan con M2
