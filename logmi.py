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
with st.form('Login Minec'):
    usuario = st.text_input('Usuario', placeholder='nombre de usuario')
    clave = st.text_input('Clave de acceso 	:key:', type="password", placeholder='clave de acceso')
    enviar = st.form_submit_button('Enviar')
    if enviar:
        buser = [x for x in res.items if x['user']==usuario]
        if len(buser)>0:
            bclave = buser[0]['clave']
            bclave
            if str(bclave)==str(clave):
                logina = buser[0]
                st.session_state['logina'] = logina
                st.write(logina)
                if buser[0]['tipou']=='AdminFinanzas':
                    switch_page('checkpay')
                else:
                    switch_page('BienvenidaU')
                
            else:
                st.write('Clave Invalida', clave, type(clave), bclave, type(bclave))
        else:
            st.write('**** Datos Invalidos **** ')
            st.write(' ⚠️  Intenta nuevamente  ')
    
    
