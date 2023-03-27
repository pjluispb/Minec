
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
    db_content = encprof.fetch({'Distrito':dtto}).items
else:
    db_content = encprof.fetch().items
    
#st.write(dtto, len(dtto))
#st.write(db_content)

distritos = ['Andino', 'Centro', 'Centro Llanos', 'Falcón', 'Lara', 'Llanos', 'Llanos Occidentales', 'Metropolitano', 'Nor Oriente', 'Sur Oriente', 'Yaracuy', 'Zulia']
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

    minCNo = len(df[(df['Categoria']=='Ministro Cristiano') & (df['paycon']=='NO')])
    minCSi = len(df[(df['Categoria']=='Ministro Cristiano') & (df['paycon']=='SI')])
    minCPend = len(df[(df['Categoria']=='Ministro Cristiano') & (df['paycon']=='PENDIENTE')])

    minLNo = len(df[(df['Categoria']=='Ministro Licenciado') & (df['paycon']=='NO')])
    minLSi = len(df[(df['Categoria']=='Ministro Licenciado') & (df['paycon']=='SI')])
    minLPend = len(df[(df['Categoria']=='Ministro Licenciado') & (df['paycon']=='PENDIENTE')])

    minONo = len(df[(df['Categoria']=='Ministro Ordenado') & (df['paycon']=='NO')])
    minOSi = len(df[(df['Categoria']=='Ministro Ordenado') & (df['paycon']=='SI')])
    minOPend = len(df[(df['Categoria']=='Ministro Ordenado') & (df['paycon']=='PENDIENTE')])

    dftot = pd.DataFrame([(minC, minCNo, minCPend, minCSi),
                          (minL, minLNo, minLPend, minLSi),
                          (minO, minONo, minOPend, minOSi)],
                          index=['Ministro Cristiano', 'Ministro Licenciado', 'Ministro Ordenado'],
                          columns=('Total','NO registrados', 'Pendientes', 'Registrados'))
    options = {
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "legend": {"data": ["No Registrado", "Pendiente",  "Registrado"]},
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "xAxis": {"type": "value"},
        "yAxis": {"type": "category", "data": ['M. Cristiano', 'M. Licenciado', 'M. Ordenado'],},
        "series": [
            {"name": "No Registrado","type": "bar","stack": "total","label": {"show": True}, 
             "emphasis": {"focus": "series"}, "data": [minCNo,minLNo,minONo],},
            {"name": "Pendiente", "type": "bar", "stack": "total","label": {"show": True}, 
             "emphasis": {"focus": "series"}, "data": [minCPend,minLPend,minOPend],},
            {"name": "Registrado", "type": "bar","stack": "total","label": {"show": True}, 
             "emphasis": {"focus": "series"}, "data":  [minCSi,minLSi,minOSi],},
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
            # fila minC
            minCNo = len(dfdtto[(dfdtto['Categoria']=='Ministro Cristiano') & (dfdtto['paycon']=='NO')])
            minCSi = len(dfdtto[(dfdtto['Categoria']=='Ministro Cristiano') & (dfdtto['paycon']=='SI')])
            minCPend = len(dfdtto[(dfdtto['Categoria']=='Ministro Cristiano') & (dfdtto['paycon']=='PENDIENTE')])
            # fila minL
            minLNo = len(dfdtto[(dfdtto['Categoria']=='Ministro Licenciado') & (dfdtto['paycon']=='NO')])
            minLSi = len(dfdtto[(dfdtto['Categoria']=='Ministro Licenciado') & (dfdtto['paycon']=='SI')])
            minLPend = len(dfdtto[(dfdtto['Categoria']=='Ministro Licenciado') & (dfdtto['paycon']=='PENDIENTE')])
            # minO
            minONo = len(dfdtto[(dfdtto['Categoria']=='Ministro Ordenado') & (dfdtto['paycon']=='NO')])
            minOSi = len(dfdtto[(dfdtto['Categoria']=='Ministro Ordenado') & (dfdtto['paycon']=='SI')])
            minOPend = len(dfdtto[(dfdtto['Categoria']=='Ministro Ordenado') & (dfdtto['paycon']=='PENDIENTE')])
            dftotXdtto = pd.DataFrame([(minC, minCNo, minCPend, minCSi),
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
                 "emphasis": {"focus": "series"}, "data": [minCNo,minLNo,minONo],},
                {"name": "Pendiente", "type": "bar", "stack": "total","label": {"show": True}, 
                 "emphasis": {"focus": "series"}, "data": [minCPend,minLPend,minOPend],},
                {"name": "Registrado", "type": "bar","stack": "total","label": {"show": True}, 
                 "emphasis": {"focus": "series"}, "data":  [minCSi,minLSi,minOSi],},
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

