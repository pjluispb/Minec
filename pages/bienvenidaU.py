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
if logina['tipou']=='AdminRegistro':
    st.write('Eres _Representante de Minec_ para todos los distritos')
else:
    st.write('Eres  _Representante de MINEC_ para el distrito ****' + logina['Distrito'] + '**** y por eso puedes ver la data del distrito y actualizar algunos registros')
st.subheader('Que deseas hacer?')
if logina['tipou']=='AdminRegistro':
    acciones = ['⏩', 'VER DATA', 'ACTUALIZAR', 'REGISTRAR', 'ACTUALIZAR SIN CÉDULA' ]
else:
    acciones = ['⏩', 'VER DATA', 'ACTUALIZAR' ]
st.write('Seleccionar Acción')
selector = st.radio('****Seleccionar Acción****', acciones, horizontal=True, label_visibility='collapsed',)
#st.write(selector)
if selector=='ACTUALIZAR':
    st.write('Actualizar Data')
    switch_page('askCed-deta')
if selector=='ACTUALIZAR SIN CÉDULA':
    st.write('Actualizar Data')
    switch_page('updauser02')
if selector=='REGISTRAR':
    switch_page('newReg-deta')
if selector=='VER DATA':
    switch_page('verdata')
  

regresar = st.button('Volver')
if regresar:
    switch_page('logmi')
