

import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from deta import Deta
from streamlit_echarts import st_echarts
import numpy as np
#import plotly.express as px
from PIL import Image

def vcountsTOdf(dataf, colname):
    salida = dataf[colname].value_counts()
    salidaDict = salida.to_dict()
    listasal = []
    for key, value in salidaDict.items():
        reg = {'Item':key, 'Valor':value }
        listasal.append(reg)
    dfSalida = pd.DataFrame(listasal)
    return(dfSalida)

def TotXModalidad(distrito):
    if distrito in Distritos:
        df_dtto   =   df[df.Distrito == distrito]
    else:
        df_dtto = df
    MC_dtto = df_dtto[df_dtto.Categoria == 'Ministro Cristiano']
    MD_dtto = df_dtto[df_dtto.Categoria == 'Ministro Distrital']
    ML_dtto = df_dtto[df_dtto.Categoria == 'Ministro Licenciado']
    MO_dtto = df_dtto[df_dtto.Categoria == 'Ministro Ordenado']
    mindtto = vcountsTOdf(df_dtto, 'Categoria')
    moddtto = vcountsTOdf(df_dtto, 'Modalidad')
    modMC_dtto = vcountsTOdf(MC_dtto, 'Modalidad')
    modMD_dtto = vcountsTOdf(MD_dtto, 'Modalidad')
    modML_dtto = vcountsTOdf(ML_dtto, 'Modalidad')
    modMO_dtto = vcountsTOdf(MO_dtto, 'Modalidad')

    st.write('-----------------------------------------')
    st.write('Distrito', distrito)
    st.write('Total ministros = ',df_dtto.shape[0],'\n')
    st.write(mindtto,'\n')
    st.write('Modalidad \n',moddtto,'\n')
    st.write('Ministro Cristiano modalidad\n',modMC_dtto,'\n')
    st.write('Ministro Distrital modalidad\n',modMD_dtto,'\n')
    st.write('Ministro Licenciado modalidad\n',modML_dtto,'\n')
    st.write('Ministro Ordenado modalidad\n',modMO_dtto,'\n')
    st.write('-----------------------------------------','\n'*2)

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')
logina = st.session_state['logina']
#logina
st.image(imagen1)
st.image(imagen2)

st.write('Hola ****' + logina['user'] + '****')
if logina['tipou']!='AdminRegistro':
    dtto = logina['Distrito']
else:
    dtto = ''
deta = Deta(st.secrets["deta_key"])

deta = Deta(st.secrets["deta_key"])

prondadb = deta.Base('ProndanminFull01')
pronda = prondadb.fetch(limit=5000)
df = pd.DataFrame(pronda.items)
df = df.iloc[:, [4,2,6,18,15]]


Distritos = ['Andino', 'Centro', 'Centro Llanos', 'Falcón', 'Lara', 'Llanos Occidentales', 'Metropolitano', 'Nor Oriente', 'Sur Oriente', 'Yaracuy', 'Zulia']
totalizadores = ['Total', 'NO registrados', 'Pendientes', 'Registrados']

TotXModalidad('TODOS')

for distrito in Distritos:
    TotXModalidad(distrito)


