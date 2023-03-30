
import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from deta import Deta
from streamlit_echarts import st_echarts

from PIL import Image

def row_style(row):
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

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')

logina = st.session_state['logina']
#logina
st.image(imagen1)
st.image(imagen2)

st.write('Hola ****' + logina['user'] + '****')
st.write('Datos del registro de ministros del distrito: ****' + logina['Distrito'] + '****')
if logina['tipou']!='AdminRegistro':
    dtto = logina['Distrito']
else:
    dtto = ''
deta = Deta(st.secrets["deta_key"])
encprof = deta.Base('ProndanminFull01')
if dtto!='':
    db_content = encprof.fetch({'Distrito':dtto}, limit=5000).items
else:
    db_content = encprof.fetch(limit=5000).items
    
#st.write(dtto, len(dtto))
#st.write(db_content)

distritos = ['Andino', 'Centro', 'Centro Llanos', 'Falcón', 'Lara', 'Llanos Occidentales', 'Metropolitano', 'Nor Oriente', 'Sur Oriente', 'Yaracuy', 'Zulia']
categorias = ['Ministro Ordenado', 'Ministro Licenciado', 'Ministro Cristiano']
totalizadores = ['Total', 'NO registrados', 'Pendientes', 'Registrados']

df = pd.DataFrame.from_dict(db_content)
df.rename(columns={"key": "cedula"}, inplace=True) # cambia el nombre de la columna KEY a CEDULA
df = df.reindex(columns=['Distrito', 'cedula', 'Nombres', 'Apellidos', 'Categoria', 'paycon', 'referenciaPago', 'fechaPago', 'montoPago', 'Email', 'Telefono', 'Modalidad', 'Status', 'ReporteCertif', 'fuenteOrigen']) #Reordena las columnas como se mostraran
df.style.apply(row_style, axis=1)  #Coloriza las filas

if dtto!='':
    minC = len(df[df['Categoria']=='Ministro Cristiano'])
    minL = len(df[df['Categoria']=='Ministro Licenciado'])
    minO  = len(df[df['Categoria']=='Ministro Ordenado'])
    minD  = len(df[df['Categoria']=='Ministro Distrital'])

    minCNo = len(df[(df['Categoria']=='Ministro Cristiano') & (df['paycon']=='NO')])
    minCSi = len(df[(df['Categoria']=='Ministro Cristiano') & (df['paycon']=='SI')])
    minCPend = len(df[(df['Categoria']=='Ministro Cristiano') & (df['paycon']=='PENDIENTE')])
    
    minDNo = len(df[(df['Categoria']=='Ministro Distrital') & (df['paycon']=='NO')])
    minDSi = len(df[(df['Categoria']=='Ministro Distrital') & (df['paycon']=='SI')])
    minDPend = len(df[(df['Categoria']=='Ministro Distrital') & (df['paycon']=='PENDIENTE')])

    minLNo = len(df[(df['Categoria']=='Ministro Licenciado') & (df['paycon']=='NO')])
    minLSi = len(df[(df['Categoria']=='Ministro Licenciado') & (df['paycon']=='SI')])
    minLPend = len(df[(df['Categoria']=='Ministro Licenciado') & (df['paycon']=='PENDIENTE')])

    minONo = len(df[(df['Categoria']=='Ministro Ordenado') & (df['paycon']=='NO')])
    minOSi = len(df[(df['Categoria']=='Ministro Ordenado') & (df['paycon']=='SI')])
    minOPend = len(df[(df['Categoria']=='Ministro Ordenado') & (df['paycon']=='PENDIENTE')])

    dftot = pd.DataFrame([(minC, minCNo, minCPend, minCSi),
                          (minD, minDNo, minDPend, minDSi),
                          (minL, minLNo, minLPend, minLSi),
                          (minO, minONo, minOPend, minOSi)],
                          index=['Ministro Cristiano', 'Ministro Distrital', 'Ministro Licenciado', 'Ministro Ordenado'],
                          columns=('Total','NO registrados', 'Pendientes', 'Registrados'))
    options = {
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "legend": {"data": ["No Registrado", "Pendiente",  "Registrado"]},
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "xAxis": {"type": "value"},
        "yAxis": {"type": "category", "data": ['M. Cristiano', 'M. Licenciado', 'M. Ordenado'],},
        "series": [
            {"name": "No Registrado","type": "bar","stack": "total","label": {"show": True}, 
                 "emphasis": {"focus": "series"}, "data": [minCNo,minDNo,minLNo,minONo],},
                {"name": "Pendiente", "type": "bar", "stack": "total","label": {"show": True}, 
                 "emphasis": {"focus": "series"}, "data": [minCPend,minDPend,minLPend,minOPend],},
                {"name": "Registrado", "type": "bar","stack": "total","label": {"show": True}, 
                 "emphasis": {"focus": "series"}, "data":  [minCSi,minDSi,minLSi,minOSi],},
        ],
    }
        


    with st.expander('Consolidado del distrito ' + dtto):
        st.subheader('Resumen '+dtto)
        st.dataframe(dftot)
        st.subheader('Gráfico '+dtto)
        st_echarts(options=options, height = '250px')
    
else:
    totales = [len(df[df['Categoria']==categoria]) for categoria in categorias]
    #print(totales, type(totales))
    paycons = ['SI','NO','PENDIENTE']
    with st.expander('Ver consolidado de todos los distritos'):
        for distto in distritos:
            dfdtto = df[df['Distrito']==distto]
            # totales
            minC = len(dfdtto[dfdtto['Categoria']=='Ministro Cristiano'])
            minL = len(dfdtto[dfdtto['Categoria']=='Ministro Licenciado'])
            minO  = len(dfdtto[dfdtto['Categoria']=='Ministro Ordenado'])
            minD  = len(dfdtto[dfdtto['Categoria']=='Ministro Distrital'])
            minD2 = dfdtto.loc[(dfdtto['Categoria'] == 'Ministro Distrital')].shape[0]
            # fila minC
            minCNo = dfdtto.loc[(df['Categoria'] == 'Ministro Cristiano') & (dfdtto['paycon'] == 'NO')].shape[0]
            minCSi = dfdtto.loc[(df['Categoria'] == 'Ministro Cristiano') & (dfdtto['paycon'] == 'SI')].shape[0]
            minCPend = dfdtto.loc[(df['Categoria'] == 'Ministro Cristiano') & (dfdtto['paycon'] == 'PENDIENTE')].shape[0]
            # fila minD
            minDNo = dfdtto.loc[(df['Categoria'] == 'Ministro Distrital') & (dfdtto['paycon'] == 'NO')].shape[0]
            minDSi = dfdtto.loc[(df['Categoria'] == 'Ministro Distrital') & (dfdtto['paycon'] == 'SI')].shape[0]
            minDPend = dfdtto.loc[(df['Categoria'] == 'Ministro Distrital') & (dfdtto['paycon'] == 'PENDIENTE')].shape[0]
            # fila minL
            minLNo = dfdtto.loc[(df['Categoria'] == 'Ministro Licenciado') & (dfdtto['paycon'] == 'NO')].shape[0]
            minLSi = dfdtto.loc[(df['Categoria'] == 'Ministro Licenciado') & (dfdtto['paycon'] == 'SI')].shape[0]
            minLPend = dfdtto.loc[(df['Categoria'] == 'Ministro Licenciado') & (dfdtto['paycon'] == 'PENDIENTE')].shape[0]
            # minO
            minONo = dfdtto.loc[(df['Categoria'] == 'Ministro Ordenado') & (dfdtto['paycon'] == 'NO')].shape[0]
            minOSi = dfdtto.loc[(df['Categoria'] == 'Ministro Ordenado') & (dfdtto['paycon'] == 'SI')].shape[0]
            minOPend = dfdtto.loc[(df['Categoria'] == 'Ministro Ordenado') & (dfdtto['paycon'] == 'PENDIENTE')].shape[0]
            
            dftotXdtto = pd.DataFrame([(minC, minCNo, minCPend, minCSi), (minD, minDNo, minDPend, minDSi),
                                (minL, minLNo, minLPend, minLSi),
                                (minO, minONo, minOPend, minOSi)],
                                index=['Ministros Cristianos', 'Ministros Licenciados', 'Ministros Ordenados'],
                                columns=('Total', 'NO registrados', 'Pendientes', 'Registrados'))
            options = {
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
            "legend": {"data": ["No Registrado", "Pendiente",  "Registrado"]},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            "xAxis": {"type": "value"},
            "yAxis": {"type": "category", "data": ['M. Cristiano', 'M. Licenciado', 'M. Ordenado'],},
            "series": [
                {"name": "No Registrado","type": "bar","stack": "total","label": {"show": True}, 
                 "emphasis": {"focus": "series"}, "data": [minCNo,minDNo,minLNo,minONo],},
                {"name": "Pendiente", "type": "bar", "stack": "total","label": {"show": True}, 
                 "emphasis": {"focus": "series"}, "data": [minCPend,minDPend,minLPend,minOPend],},
                {"name": "Registrado", "type": "bar","stack": "total","label": {"show": True}, 
                 "emphasis": {"focus": "series"}, "data":  [minCSi,minDSi,minLSi,minOSi],},
            ],
        }
        
            st.subheader(distto)
            st.dataframe(dftotXdtto)
            st_echarts(options=options, height = '250px')
            st.write('---')
    
with st.expander('Data del distrito ' + dtto):
    df = df.reindex(columns=['Distrito', 'Categoria', 'cedula', 'Nombres', 'Apellidos', 'paycon', 'Modalidad', 'MontoApagar', 'montoPago', 'Diferencia', 'fuenteOrigen', 'referenciaPago', 'fechaPago', 'Email', 'Telefono'])
    st.dataframe(df.style.apply(row_style, axis=1))
    
regresar = st.button('Volver')
if regresar:
    switch_page('logmi')

