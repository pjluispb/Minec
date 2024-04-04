import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from deta import Deta
from PIL import Image

deta = Deta(st.secrets["deta_key"])
accesos = deta.Base('minec-accesos')
res=accesos.fetch()
#res.items

st.set_page_config(
    page_title="Minec Reg App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)


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
        buser = [x for x in res.items if (x['user']==usuario and x['clave']==clave)]
        #st.write(buser)
        if len(buser)>0:
            bclave = buser[0]['clave']
            #bclave2 = [y for y in buser if y['clave'].startswith('vov4-')]
            #print(bclave)

            if str(bclave).startswith('vov4-'):
                if str(bclave)==str(clave):
                    logina = buser[0]
                    st.session_state['logina'] = logina
                    st.write(logina)
                    if buser[0]['tipou']=='AdminFinanzas':
                        switch_page('checkpay')
                    else:
                        switch_page('BienvenidaU2024')
                else: st.write('Clave Inválida')
            else:
                st.toast('Clave Inválida')
                #st.write('Clave Invalida', clave, type(clave), bclave, type(bclave))
        else:
            st.write('Nombre de Usuario Invalido')
st.page_link("pages/home2024.py", label="Inicio", icon="🏠")
    
