
import pygsheets
import pandas as pd
from deta import Deta
import random
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import time
from google.oauth2 import service_account

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')
def inicializaConexiones():
    deta = Deta(st.secrets.deta_key)
    SCOPES = ('https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive')
    service_account_info = st.secrets.gcp_service_account
    my_credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes = SCOPES)
    gc =pygsheets.authorize(custom_credentials=my_credentials)
    accesos = deta.Base('minec-accesos')
    res=accesos.fetch()
    return deta, gc, res

def row_style(row):
    if row['confirmado'] == 'SI':
        return pd.Series('background-color: #8ede99; color:#000000', row.index)
    else:
        return pd.Series('', row.index)
    
def row_style2(row):
    if row['paycon'] == 'SI':
        return pd.Series('background-color: #8ede99; color:#000000', row.index)
    elif row['paycon'] == 'PENDIENTE':
        return pd.Series('background-color: #fdd834; color:#000229', row.index)
    else:
        return pd.Series('', row.index)
    
logina = st.session_state['logina']
deta, gc, res = inicializaConexiones()

paycdb = deta.Base('payconf')
payc = paycdb.fetch()
prondadb = deta.Base('ProndanminFull01')
pronda = prondadb.fetch()

progress_text = "Realizando el match entre usuarios y pagos. Por favor espere un momento"
my_bar = st.progress(0, text=progress_text)
for percent_complete in range(100):
    time.sleep(0.03)
    my_bar.progress(percent_complete + 1, text=progress_text)

dfpay = pd.DataFrame(payc.items)
dfpron = pd.DataFrame(pronda.items)
dfpay = dfpay.drop('key', axis=1)
dfpay.style.apply(row_style, axis=1)  #Coloriza las filas
with st.expander('Tabla de pagos'):
    st.dataframe(dfpay.style.apply(row_style, axis=1))
pendientes = [registro for registro in pronda.items if registro['paycon']=='PENDIENTE']
dfpendientes = pd.DataFrame(pendientes)
# print('\n'*3, dfpendientes)
# print('\n'*5, 'Haciendo Match')
for index, row in dfpendientes.iterrows():
        # print(row['referenciaPago'])
        refbuscada = paycdb.fetch({"key":str(row['referenciaPago'])})
        if len(refbuscada.items) > 0:
                regProndXupd = {'paycon':'SI'}
                clavePronda = str(row['key'])
                regPaycXupd = {'confirmado':'SI', 'nroFuente':str(row['key'])}
                clavePayc = refbuscada.items[0]['key']
                # print('Actualiza en Payconf registro clave', clavePayc, 'con los datos :', regPaycXupd)
                paycdb.update(regPaycXupd, clavePayc)
                # print('Actualiza en ProndaminFull registro clave', clavePronda, 'con los datos :', regProndXupd)
                prondadb.update(regProndXupd, clavePronda)

with st.expander('Tabla de usuarios'):
    st.dataframe(dfpron.style.apply(row_style2, axis=1))

regresar = st.button('Volver')
if regresar:
    switch_page('logmi')
