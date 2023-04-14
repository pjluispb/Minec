

import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from deta import Deta
from streamlit_echarts import st_echarts
import numpy as np
#import plotly.express as px
from PIL import Image
from streamlit_echarts import st_echarts
#import plotly.figure_factory as ff


def vcountsTOdf(dataf, colname):
    salida = dataf[colname].value_counts()
    salidaDict = salida.to_dict()
    listasal = []
    for key, value in salidaDict.items():
        reg = {'Item':key, 'Valor':value }
        listasal.append(reg)
    dfSalida = pd.DataFrame(listasal)
    return(dfSalida)

def vcountsTOlistXgrafi(dataf, colname):
    salida = dataf[colname].value_counts()
    salidaDict = salida.to_dict()
    listXgraf = []
    for key, value in salidaDict.items():
        regrafi = {'value':value, 'name':key}
        listXgraf.append(regrafi)
    #dfSalida = pd.DataFrame(listasal)
    return(listXgraf)

def vcountsTOlist(ministros, dataf, colname):
    salida = dataf[colname].value_counts()
    salidaDict = salida.to_dict()
    listasal = []
    for key, value in salidaDict.items():
        reg = (ministros, key, value)
        listasal.append(reg)
    #dfSalida = pd.DataFrame(listasal)
    return(listasal)

def TotXModalidad(distrito):
    if distrito in Distritos:
        df_dtto   =   df[df.Distrito == distrito]
    else:
        df_dtto = df
        datap = vcountsTOlistXgrafi(df_dtto,'Categoria')
        option05 = { 
            #   'backgroundColor': '#100C2A',
        'title': { 'text': 'Ministros 2023', 'left': 'center'  },
        'tooltip': {    'trigger': 'item'  },
        # 'legend': {    'orient': 'vertical',    'left': 'left'  },
        'series': [    
            {  'name': 'Ministros',      'type': 'pie',      'radius': '75%',
            'data': datap,
            'emphasis': { 'itemStyle': { 'shadowBlur': 10, 'shadowOffsetX': 0,  'shadowColor': 'rgba(0, 0, 0, 0.5)'  } }
            }  ]   }
    MC_dtto = df_dtto[df_dtto.Categoria == 'Ministro Cristiano']
    MD_dtto = df_dtto[df_dtto.Categoria == 'Ministro Distrital']
    ML_dtto = df_dtto[df_dtto.Categoria == 'Ministro Licenciado']
    MO_dtto = df_dtto[df_dtto.Categoria == 'Ministro Ordenado']
    mindtto = vcountsTOdf(df_dtto, 'Categoria')
    moddtto = vcountsTOdf(df_dtto, 'Modalidad')
    lmod = vcountsTOlist('Total Ministros ',df_dtto, 'Modalidad')
    #-------------------------------------------------------
    lmodXgraf = vcountsTOlistXgrafi(df_dtto,'Categoria')
    option06 = { 
            #   'backgroundColor': '#100C2A',
        #'title': { 'text': 'Ministros 2023', 'left': 'center'  },
        'tooltip': {    'trigger': 'item'  },
        # 'legend': {    'orient': 'vertical',    'left': 'left'  },
        'series': [    
            {  'name': 'Ministros',      'type': 'pie',      'radius': '75%',
            'data': lmodXgraf,
            'emphasis': { 'itemStyle': { 'shadowBlur': 10, 'shadowOffsetX': 0,  'shadowColor': 'rgba(0, 0, 0, 0.5)'  } }
            }  ]   }
    #-------------------------------------------------------
    modMC_dtto = vcountsTOdf(MC_dtto, 'Modalidad')
    lmodMC = vcountsTOlist('Ministro Cristiano',MC_dtto, 'Modalidad')
    modMD_dtto = vcountsTOdf(MD_dtto, 'Modalidad')
    lmodMD = vcountsTOlist('Ministro Distrital',MD_dtto, 'Modalidad')
    modML_dtto = vcountsTOdf(ML_dtto, 'Modalidad')
    lmodML = vcountsTOlist('Ministro Licenciado',ML_dtto, 'Modalidad')
    modMO_dtto = vcountsTOdf(MO_dtto, 'Modalidad')
    lmodMO = vcountsTOlist('Ministro Ordenado',MO_dtto, 'Modalidad')
    lmodComb = lmod+lmodMC+lmodMD+lmodML+lmodMO
    
    dflmodComb = pd.DataFrame(lmodComb)
    # st.write(dflmodComb.columns, dflmodComb.index)
    # dflmodComb.rename(str, axis='columns')
    # st.write(dflmodComb.columns)
    dflmodComb.columns =['Categoría', 'Modalidad', 'Participantes']
    #dflmodComb.set_index('Categoria')
    #df_centered = dflmodComb.apply(lambda x: x-x.mean())
    Virtuales = dflmodComb[dflmodComb.Modalidad == 'Virtual']
    VirtualesLista = Virtuales.Participantes.to_list()
    Presenciales = dflmodComb[dflmodComb.Modalidad == 'Presencial']
    PresencialesLista = Presenciales.Participantes.to_list()
    NoInscritos = dflmodComb[dflmodComb.Modalidad == '-']
    NoInscritosLista = NoInscritos.Participantes.to_list()
    option07 = {
  'tooltip': { 'trigger': 'axis','axisPointer': { 'type': 'shadow' }},
  #'legend': {},
  'grid': { 'left': '3%', 'right': '4%', 'bottom': '3%', 'containLabel': 'true'   },
  'xAxis': {  'type': 'value'   },
  'yAxis': {  'type': 'category',  'data': ['Total', 'Cristiano', 'Distrital', 'Licenciado', 'Ordenado']   },
  'series': [
    { 'name': 'Virtual', 'type': 'bar', 'stack': 'total',
      'label': { 'show': 'true' },
      'emphasis': { 'focus': 'series'       },
      'data': VirtualesLista},
    { 'name': 'Presencial', 'type': 'bar',  'stack': 'total',
      'label': { 'show': 'true'  },
      'emphasis': { 'focus': 'series'  },
      'data': PresencialesLista },
    { 'name': 'NO inscrito',  'type': 'bar', 'stack': 'total',
      'label': { 'show': 'true' },
      'emphasis': { 'focus': 'series' },
      'data': NoInscritosLista }
         ]
        }
    #st.write('Virtuales',Virtuales,VirtualesLista)

    st.write('-----------------------------------------')
    col1, col2 = st.columns(2)
    with col1:
        st.write('Distrito', distrito)
        st.write('Total ministros = ',df_dtto.shape[0],'\n')
        st.write(mindtto,'\n')
        st.write(dflmodComb)
    with col2:
        # if distrito=='TODOS':
        #     st_echarts(options=option05, height="300px")
        st_echarts(options=option06, height="300px")
        # VirtualesLista
        # PresencialesLista
        # NoInscritosLista
        st_echarts(options=option07, height="300px")

    
    # st.write('Modalidad \n',moddtto,'\n')
    # st.write('Ministro Cristiano modalidad\n',modMC_dtto,'\n')
    # st.write('Ministro Distrital modalidad\n',modMD_dtto,'\n')
    # st.write('Ministro Licenciado modalidad\n',modML_dtto,'\n')
    # st.write('Ministro Ordenado modalidad\n',modMO_dtto,'\n')
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

distrito = 'TODOS'
if distrito not in Distritos:
        df_dtto = df
        datap = vcountsTOlistXgrafi(df_dtto,'Categoria')

option05 = { 
    #   'backgroundColor': '#100C2A',
  'title': { 'text': 'Ministros 2023', 'left': 'center'  },
  'tooltip': {    'trigger': 'item'  },
 # 'legend': {    'orient': 'vertical',    'left': 'left'  },
  'series': [    
    {  'name': 'Ministros',      'type': 'pie',      'radius': '70%',
      'data': datap,
      'emphasis': { 'itemStyle': { 'shadowBlur': 10, 'shadowOffsetX': 0,  'shadowColor': 'rgba(0, 0, 0, 0.5)'  } }
    }  ]   }

#st_echarts(options=option05, height="200px")
