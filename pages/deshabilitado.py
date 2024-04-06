

import time
import requests
from deta import Deta
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
from streamlit_extras.switch_page_button import switch_page
from PIL import Image


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

deta = Deta(st.secrets["deta_key"])
minecAccess = deta.Base('minec-accesos')
minecAccessDb = minecAccess.fetch()
clavesper = minecAccessDb.items
clavesper2 = [x['clave'] for x in  clavesper]

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')

lottie_url_manteniniento = "https://assets9.lottiefiles.com/packages/lf20_hxpynlxn.json"
lottie_url_notifi = "https://assets6.lottiefiles.com/temp/lf20_MIzQDr.json"
lottie_url_processing = "https://assets9.lottiefiles.com/private_files/lf30_4mv84cax.json"
lottie_url_processing02 = "https://assets8.lottiefiles.com/packages/lf20_TwMAB48r0t.json"
lottie_url_processing03 = "https://assets8.lottiefiles.com/temp/lf20_x0S70Z.json"
lottie_url_processing05 = "https://lottiefiles.com/90534-spinner"
lottie_url_processing07 = "https://assets3.lottiefiles.com/packages/lf20_9N6oCY.json"
lottie_mantenimiento = load_lottieurl(lottie_url_manteniniento)
lottie_notifi = load_lottieurl(lottie_url_notifi)
lottie_processing = load_lottieurl(lottie_url_processing)
lottie_processing02 = load_lottieurl(lottie_url_processing02)
lottie_processing03 = load_lottieurl(lottie_url_processing03)
#lottie_processing05 = load_lottieurl(lottie_url_processing05)
lottie_processing07 = load_lottieurl(lottie_url_processing07)

#st_lottie(lottie_hello, key="hello")
#st_lottie(lottie_processing, key='processing')


cola, colb, colc =st.columns(3)
col1, col2 = st.columns(2)
with cola:
    st.image(imagen1)
    st.image(imagen2)
with colb:
    st_lottie(lottie_notifi)
with colc:
    st.write('***')
    
with col2:
    st.subheader('Sentimos informar que actualmente el :orange[sistema de registro] para los cursos de actualización ministerial :blue[PRONDAMIN2023], está :red[deshabilitado] :orange[temporalmente] . Por favor intente ingresar més tarde.')
    #st.subheader('Sentimos informar que actualmente el :orange[sistema de registro] para los cursos de actualización ministerial :blue[PRONDAMIN2023], está en :red[mantenimiento] y ha sido :red[deshabilitado] :orange[temporalmente]. Por favor intente ingresar más tarde.')
with col1:
    st_lottie(lottie_mantenimiento)

# if st.button("Download"):
    #with st_lottie_spinner(lottie_download, key="download"):
#     with st_lottie_spinner(lottie_processing07, key="processing07"):
#          time.sleep(20)
#     st.balloons()
st.write('---')
claveUminec = st.text_input(label='', max_chars=10)
if claveUminec in clavesper2:
    st.session_state['logEsp']=claveUminec
    st.balloons()
    switch_page("updauser")
