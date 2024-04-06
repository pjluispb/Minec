
import streamlit as st

#from deta import Deta
from PIL import Image

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')

st.image(imagen1)
st.image(imagen2)

st.header('Bienvenido a MINEC')
st.subheader('Ministerio de Educación Cristiana de las Asambleas de Dios Venezuela')
ingresou = st.popover(' $$ \large 👉PRONDAMIN 2024👈 \\newline Ingresar $$')

uministro = ingresou.toggle(' $$ \Large Ministro \small \\newline Ministro \,acreditado \,que \,desee \\newline actualizar \,su \,data \,y/o \,\, inscribirse \\newline en \,curso \,PRONDAMIN $$')
uminec = ingresou.toggle(' $$ \large Usuario \,MINEC $$')


if uminec:
    #st.switch_page('logmi.py')
    st.switch_pages('pages/deshabilitado.py')
if uministro:
    #st.switch_page('pages/logministro.py')
    st.switch_page('pages/deshabilitado.py')
