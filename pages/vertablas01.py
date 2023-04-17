
import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from deta import Deta
from streamlit_echarts import st_echarts
from PIL import Image
from google.oauth2 import service_account
import pygsheets
from pathlib import Path

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')

try:
    logina = st.session_state['logina']
except:
    switch_page('reiniciar03')


def Conexiones():
    deta = Deta(st.secrets["deta_key"])
    SCOPES = ('https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive')
    service_account_info = st.secrets.gcp_service_account
    my_credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes = SCOPES)
    gc =pygsheets.authorize(custom_credentials=my_credentials)
    return deta, gc

st.image(imagen1)
st.image(imagen2)
deta, gc = Conexiones()

permisados=[]
resdb = deta.Base('minec-accesos')
res = resdb.fetch()
for t in range(len(res.items)):
    if res.items[t]['tipou']=='AdminRegistro':
        permisados.append((res.items[t]['user'], res.items[t]['clave']))
if (logina['user'], logina['clave']) not in permisados:
    st.write('No esta en permisados')
    switch_page('reiniciar03')

st.subheader('Generar tablas por Distrito y Modalidad')
with st.form(key='SelTabla'):
    tipoMod = st.radio(label = 'Seleccione Modalidad', options=['Virtual','Presencial','Ninguna (NO inscritos aún)'], index=0, horizontal=True)
    dtto = st.radio(label='Seleccione el Distrito',options=['Andino', 'Centro', 'Centro Llanos', 'Falcón', 'Lara', 'Llanos', 'Llanos Occidentales', 'Metropolitano', 'Nor Oriente', 'Sur Oriente', 'Yaracuy', 'Zulia', 'Todos'], horizontal=True)
    if tipoMod == 'Ninguna (NO inscritos aún)': modtab='NOins'
    else: modtab=tipoMod
    nameTable = 'listado'+dtto+modtab+'.csv'
    #nameTable
    
    enviar = st.form_submit_button('Generar')
    if enviar:
        prondadb = deta.Base('ProndanminFull01')
        pronda = prondadb.fetch(limit=5000)
        df = pd.DataFrame(pronda.items)
        if tipoMod=='Ninguna (NO inscritos aún)': tipoMod='-'
        df = df.loc[:, ['Distrito', 'Modalidad', 'Categoria',  'key', 'Nombres', 'Apellidos','Email','correo','paycon','montoPago','referenciaPago']]
        if dtto != 'Todos':
            df = df.loc[(df['Distrito'] == dtto) & (df['Modalidad'] == tipoMod)]
        st.subheader('Tabla de datos correspondiente al distrito: :blue['+dtto+'] en la modalidad: :orange['+modtab+']')
        st.dataframe(df)
        #path = Path.cwd()/nameTable
        #st.write('La tabla generada se guardó como: ', path)
        #df.to_csv(path)

        # Open spreadsheet and select worksheet
        listado = 'li'+dtto
        #listado
        #modtab
        sh = gc.open(listado)
        wks = sh.worksheet_by_title(modtab)
        # Write data to worksheet
        wks.set_dataframe(df, start='A1')
        
regresar = st.button('Volver')
if regresar:
    switch_page('logmi')      

