import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from deta import Deta
from PIL import Image

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')

deta = Deta(st.secrets["deta_key"])
accesos = deta.Base('minec-accesos')
res=accesos.fetch()
#res.items
logina = st.session_state['logina']

st.image(imagen1)
st.image(imagen2)
st.subheader('Bienvenid@ ' + logina['user'])
st.write('Eres ****' + logina['tipou'] + '**** y puedes editar datos del distrito: ****' + logina['Distrito'] + '****')
st.subheader('Que deseas hacer?')

acciones = ['⏩','ACTUALIZAR', 'REGISTRAR', 'VER DATA']
st.write('Seleccionar Accion')
selector = st.radio('****Seleccionar Acción****', acciones, horizontal=True, label_visibility='collapsed',)
#st.write(selector)
if selector=='ACTUALIZAR':
    st.write('Actualizar Data')
    switch_page('askCed-deta')
if selector=='REGISTRAR':
    switch_page('newReg-deta')
if selector=='VER DATA':
    switch_page('verdata')