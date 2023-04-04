
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

def eanumber(string_var):
    x=[]
    for i in string_var.split():
        i = i.replace(',','.')
        i = i.replace(':',' ')
        #print('i =',i)
        try:
            x.append(float(i))
        except ValueError :
            pass
    return(x)

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
    if row['confirmado'] == 'SI++':
        return pd.Series('background-color: #7986cb; color:#000000', row.index)
    elif row['confirmado'] == 'PENDIENTE x DIFERENCIA':
        return pd.Series('background-color: #ff6f00; color:#000000', row.index)
    elif row['confirmado'] == 'SI':
        return pd.Series('background-color: #8ede99; color:#000000', row.index)
    elif row['confirmado'] == 'PENDIENTE':
        return pd.Series('background-color: #fdd834; color:#000000', row.index)
    else:
        return pd.Series('', row.index)
    
def row_style2(row):
    if row['paycon'] == 'SI++':
        return pd.Series('background-color: #7986cb; color:#000000', row.index)
    elif row['paycon'] == 'PENDIENTE x DIFERENCIA':
        return pd.Series('background-color: #ff6f00; color:#000000', row.index)
    elif row['paycon'] == 'SI':
        return pd.Series('background-color: #8ede99; color:#000000', row.index)
    elif row['paycon'] == 'PENDIENTE':
        return pd.Series('background-color: #fdd834; color:#000000', row.index)
    else:
        return pd.Series('', row.index)
try:   
    logina = st.session_state['logina']
except:
    st.write('se ha perdido la conexion')
deta, gc, res = inicializaConexiones()

paycdb = deta.Base('payconf')
payc = paycdb.fetch()
prondadb = deta.Base('ProndanminFull01')
pronda = prondadb.fetch(limit=5000)
montopay = deta.Base('MontoAPagar')
montoApagar = montopay.fetch()
margenp = montoApagar.items[0]['margenp']

progress_text = "Realizando el match entre usuarios y pagos. Por favor espere un momento"
my_bar = st.progress(0, text=progress_text)
for percent_complete in range(100):
    time.sleep(0.03)
    my_bar.progress(percent_complete + 1, text=progress_text)

dfpay = pd.DataFrame(payc.items)
dfpron = pd.DataFrame(pronda.items)
dfpay = dfpay.drop('key', axis=1)
dfpay.style.apply(row_style, axis=1)  #Coloriza las filas de tabla de pagos
with st.expander('Tabla de pagos'):
    dfpay = dfpay.reindex(columns=['REFERENCIA', 'DESCRIPCION', 'FECHA', 'INGRESO', 'montoApagar', 'Diferencia', 'confirmado', 'nroFuente'])
    st.dataframe(dfpay.style.apply(row_style, axis=1))
    #st.dataframe(dfpay)
#pronda.items
#dfpron
try:
    pendientes = [registro for registro in pronda.items if registro['paycon']=='PENDIENTE']
except:
     st.write('error en pendientes')
dfpendientes = pd.DataFrame(pendientes)
# print('\n'*3, dfpendientes)
# print('\n'*5, 'Haciendo Match')
for index, row in dfpendientes.iterrows():
        #st.write('referenciaPago = ',row['referenciaPago'][-4:])
        #refbuscada = paycdb.fetch({"key":str(row['referenciaPago'][-4:])})
        #if len(refbuscada.items) > 0:
        #        diferencia = float(row['MontoApagar'])-enu(row['montoPago'])
        #        if abs(diferencia)<=int(margenp): vpayc = 'SI'
        #        else:
        #             if float(row['montoPago']) > enu(row['MontoApagar']): vpayc = 'SI++'
        #             else: vpayc = 'PENDIENTE x DIFERENCIA'
        #        regProndXupd = {'paycon':vpayc,  'Diferencia':str(diferencia)}
        #        regPaycXupd ={'confirmado':vpayc, 'nroFuente':str(row['key']), 'Diferencia':str(diferencia), 'montoApagar':str(row['MontoApagar'])}
        #        st.write('diferencia = ',diferencia, 'vpayc = ',vpayc)
        #        # print('Diferencia = ',diferencia)
        #        clavePronda = str(row['key'])
        #        #regPaycXupd = {'confirmado':'SI', 'nroFuente':str(row['key'])}
        #        clavePayc = refbuscada.items[0]['key']
        refbuscada = dfpay[dfpay['REFERENCIA'].str.endswith(row['referenciaPago'][-4:])]
        if len(refbuscada) > 0:
            drefbus = refbuscada.to_dict('dict')
            #st.write('REFERENCIA : ',list(drefbus['REFERENCIA'].items())[0][1], ' - INGRESO : ',list(drefbus['INGRESO'].items())[0][1], ' - FECHA : ',list(drefbus['FECHA'].items())[0][1], ' - DESCRIPCION : ', list(drefbus['DESCRIPCION'].items())[0][1])
            #st.write('ReferenciaPago: ',row['referenciaPago'], row['Apellidos'], row['Nombres'],' Categoria: ', row['Categoria'],' ID : ', row['key'],' MontoPago : ', row['montoPago'], 'MontoApagar : ',row['MontoApagar'], row['paycon'])
            #st.write('eanumber : ', eanumber(row['montoPago'])[0])
            diferencia = round(float(row['MontoApagar'])-abs(eanumber(row['montoPago'])[0]))
            #st.write('Diferencia = ', diferencia)
            if abs(diferencia)<=int(margenp): vpayc = 'SI'
            else:
                if abs(eanumber(row['montoPago'])[0]) > float(row['MontoApagar']): vpayc = 'SI++'
                else: vpayc = 'PENDIENTE x DIFERENCIA'
            regProndXupd = {'paycon':vpayc,  'Diferencia':str(diferencia)}
            regPaycXupd ={'confirmado':vpayc, 'nroFuente':str(row['key']), 'Diferencia':str(diferencia), 'montoApagar':str(row['MontoApagar'])}
            print('diferencia = ',diferencia, 'vpayc = ',vpayc)
            clavePronda = str(row['key'])
            #st.write('ClavePronda: ', clavePronda, ' --> update--> ', regProndXupd)
            #regPaycXupd = {'confirmado':'SI', 'nroFuente':str(row['key'])}
            #clavePayc = refbuscada.items[0]['key']
            clavePayc = list(drefbus['REFERENCIA'].items())[0][1]
            #st.write('clavePayc : ',clavePayc, '-->update-->', regPaycXupd)
            # print('Actualiza en Payconf registro clave', clavePayc, 'con los datos :', regPaycXupd)
            paycdb.update(regPaycXupd, clavePayc)
            # print('Actualiza en ProndaminFull registro clave', clavePronda, 'con los datos :', regProndXupd)
            prondadb.update(regProndXupd, clavePronda)
        #else:
        #     st.write(row['referenciaPago'], 'NO encontrado')

with st.expander('Tabla de usuarios'):
    dfpron = dfpron.reindex(columns=['Distrito', 'Categoria', 'key', 'Nombres', 'Apellidos', 'paycon', 'Modalidad', 'MontoApagar', 'montoPago', 'Diferencia', 'fuenteOrigen', 'referenciaPago', 'fechaPago', 'correo', 'Telefono'])
    #df = df.sort_values(by='age', ascending=False)
    dfpron = dfpron.sort_values(by='paycon', ascending=False)
    st.dataframe(dfpron.style.apply(row_style2, axis=1))
    #st.dataframe(dfpron)

regresar = st.button('Volver')
if regresar:
    switch_page('logmi')
