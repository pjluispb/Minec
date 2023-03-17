
import pygsheets
import pandas as pd
from deta import Deta
import random
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import time

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')

def inicializaConexiones():
    #deta = Deta('e063kbj1_FY2aGBCaDSyMJYwDKW9Jcih2epyAjASb')
    deta = Deta(st.secrets["deta_key"])
    gc = pygsheets.authorize(service_file='/Users/user/Desktop/python/pystreamlit/sacred-atom-377200-804f7396d615.json')
    accesos = deta.Base('minec-accesos')
    res=accesos.fetch()
    return deta, gc, res

def getdfqfinal(gc):     
    gsheetsTit = gc.spreadsheet_titles()       #obtiene la lista de todas las gsheets
    files = [x for x in gsheetsTit if x.startswith('M2')]    #obtiene la lista de los gsheets que comienzan con M2
    #print(files)
    shs = [gc.open(titu) for titu in files]     #obtengo cada gsheet de files
    #print(shs)
    wks = [sh[0] for sh in shs]                 #obtiene la hoja 1 de cada gsheet de files
    #print(wks)
    dfs = [wk.get_as_df(include_tailing_empty=False) for wk in wks]   #convierte cada hoja(wks) en un df
    dfqs = [df.query("INGRESO != ''") for df in dfs]             #obtiene de cada df solo aquellos que tienen INGRESO y los pone en dfq
    dfqss = [dfq.convert_dtypes(infer_objects=False, convert_string=True) for dfq in dfqs]    #convierte los tipos de los dfq en cadenas(str)
    dfqfinal = []
    n = 1
    for dfq in dfqss:
        dfqfinal.append((n,dfq))
        n+=1

    return dfqfinal

logina = st.session_state['logina']
deta, gc, res = inicializaConexiones()

st.image(imagen1)
st.image(imagen2)
st.subheader('Bienvenid@ ' + logina['user'])
st.subheader('al área de Administración de Pagos')
st.subheader('Paso 1: ')
st.write('Cargando  data de pagos de la carpeta drive')
progress_text = "Leyendo la carpeta en gdrive. Por favor espere un momento"
my_bar = st.progress(0, text=progress_text)
for percent_complete in range(100):
    time.sleep(0.03)
    my_bar.progress(percent_complete + 1, text=progress_text)

paycdb = deta.Base('payconf')
payc = paycdb.fetch()

df = pd.DataFrame(payc.items)
print(df)

dfqfinal = getdfqfinal(gc)

lendfs = [len(df[1]) for df in dfqfinal]
regins, contador = [], 1
for t in dfqfinal:
    st.write('✔️','Revisando gsheet',str(contador),'✔️')
    contador+=1
    for index, row in t[1].iterrows():
        item = paycdb.get(str(row['REFERENCIA']))
        if item==None: 
            msg = '....El registro NO existe en la bd...... Accion: se insertará'
            registro = {
                "key": str(row['REFERENCIA']),
                "REFERENCIA": str(row['REFERENCIA']),
                "FECHA": str(row['FECHA']),
                "DESCRIPCION": str(row['DESCRIPCION']),
                "INGRESO": str(row['INGRESO']),
                "confirmado":'',
                "nroFuente":''
            }
            if str(row['REFERENCIA'])!='0':
                paycdb.put(registro)
                regins.append(registro)
        else: msg = '...registro ya existe en bd...... Accion: NO se insertará'

with st.expander('Registros añadidos a la BD'):
    st.write('Los siguientes',len(regins), ' registros fueron insertados en la bd')
    if len(regins)==0: print(' -------->>> ningun registro')
    else:
        for t in regins:
            st.write('REFERENCIA : ',t['REFERENCIA'])

st.subheader('Paso 2: ')
matchpyu = st.button('Match pagos y usuarios')
if matchpyu: switch_page('matchpayuser')
    
    

    

