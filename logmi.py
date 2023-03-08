import streamlit as st
from streamlit_extras.switch_page_button import switch_page
# Aplicacion base...en pagesMinec....significa que va para la raiz y el resto en el subdir pages
from deta import Deta
from PIL import Image

st.set_page_config(
    page_title="Minec Reg App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",

)

deta = Deta(st.secrets["deta_key"])
accesos = deta.Base('minec-accesos')
res=accesos.fetch()

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')
st.image(imagen1)
st.image(imagen2)

st.subheader('Login')
clave = st.text_input('Ingrese clave de acceso 	:key:', type="password")
if clave == '99999':
    acciones = ['=>','ACTUALIZAR', 'REGISTRAR', 'VER DATA']
    st.subheader('Seleccionar Accion')
    selector = st.radio('****Seleccionar Acción****', acciones, horizontal=True, label_visibility='collapsed',)
    #st.write(selector)
    if selector=='ACTUALIZAR':
        switch_page('askCed')
    if selector=='REGISTRAR':
        switch_page('newReg')
    if selector=='VER DATA':
        switch_page('verdata')
    
    
