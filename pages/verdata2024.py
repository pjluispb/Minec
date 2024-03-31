

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

def row_style_2(row):
    if row['Distrito'] in ('Andino', 'Centro Llanos', 'Lara', 'Llanos Occidentales', 'Nor Oriente', 'Yaracuy' ):
        return pd.Series('background-color: #8eddf9; color:#000000', row.index)
    else:
        return pd.Series('background-color: #eeeeee; color:#000229', row.index)

def row_style_3(row):
    if row['index']=='Ministro Licenciado' :
        return pd.Series('background-color: #eeeeee; color:#000229', row.index)

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')

try:
    logina = st.session_state['logina']
except:
    switch_page('reiniciar03')

#logina = st.session_state['logina']
#logina
st.image(imagen1)
st.image(imagen2)

st.write('Hola ****' + logina['user'] + '****')
st.write('Datos del registro de ministros del distrito: ****' + logina['Distrito'] + '****')
if logina['tipou']!='Registrador Especial':
    dtto = logina['Distrito']
else:
    dtto = ''
deta = Deta(st.secrets["deta_key"])
encprof = deta.Base('Prondamin2024A')
if dtto!='':
    db_content = encprof.fetch({'Distrito':dtto}, limit=2000).items
else:
    db_content = encprof.fetch(limit=3000).items
#st.write(db_content)
distritos = ['Andino', 'Centro', 'Centro Llanos', 'Falcón', 'Lara', 'Llanos Occidentales', 'Metropolitano', 'Nor Oriente', 'Sur Oriente', 'Yaracuy', 'Zulia']
categorias = ['Ministro Ordenado', 'Ministro Licenciado', 'Ministro Cristiano']
totalizadores = ['Total', 'NO registrados', 'Pendientes', 'Registrados']

df = pd.DataFrame.from_dict(db_content)
df.rename(columns={"key": "cedula"}, inplace=True) # cambia el nombre de la columna KEY a CEDULA
df = df.reindex(columns=['Distrito', 'Categoria', 'cedula', 'Nombres', 'Apellidos', 'Email', 'Telefono', 'Modalidad', 'paycon', 'MontoApagar', 'fuenteOrigen', 'referenciaPago', 'fechaPago', 'montoPago',   'Status', 'ReporteCertif' ]) #Reordena las columnas como se mostraran
df.style.apply(row_style, axis=1)  #Coloriza las filas
categoriasEnPron = set(df['Categoria'].tolist())
#st.write(categoriasEnPron)

if dtto!='':
    minC = len(df[df['Categoria']=='Ministro Cristiano'])
    minL = len(df[df['Categoria']=='Ministro Licenciado'])
    minO  = len(df[df['Categoria']=='Ministro Ordenado'])
    minD  = len(df[df['Categoria']=='Ministro Distrital'])
    #minotro = len(df[df['Categoria']=='Otro'])

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
            "yAxis": {"type": "category", "data": ['M. Cristiano', 'M.Distrital','M. Licenciado', 'M. Ordenado'],},
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
            #minotro = len(df[df['Categoria']=='Otro'])
            # fila minC
            # ------>>>     df.loc[(df['col1'] == value1) & (df['col2'] == value2), ['col1', 'col2']].apply(pd.Series.value_counts)
            # ------>>>            df.loc[(df['col1'] == 'MC') & (df['col2'] == 'SI')].shape[0]
            minCNo = dfdtto.loc[(df['Categoria'] == 'Ministro Cristiano') & (dfdtto['paycon'] == 'NO')].shape[0]
            minCSi = dfdtto.loc[(df['Categoria'] == 'Ministro Cristiano') & (dfdtto['paycon'] == 'SI')].shape[0]
            minCPend = dfdtto.loc[(df['Categoria'] == 'Ministro Cristiano') & (dfdtto['paycon'] == 'PENDIENTE')].shape[0]

            #minCNo =dfdtto.loc[(dfdtto['Categoria'] == 'Ministro Cristiano') & (dfdtto['paycon'] == 'NO'), ['Categoria', 'paycon']].apply(pd.Series.value_counts)
            #minCSi =dfdtto.loc[(dfdtto['Categoria'] == 'Ministro Cristiano') & (dfdtto['paycon'] == 'SI'), ['Categoria', 'paycon']].apply(pd.Series.value_counts)
            #minCPend =dfdtto.loc[(dfdtto['Categoria'] == 'Ministro Cristiano') & (dfdtto['paycon'] == 'PENDIENTE'), ['Categoria', 'paycon']].apply(pd.Series.value_counts)
            #minCNo = len(dfdtto[(dfdtto['Categoria']=='Ministro Cristiano') & (dfdtto['paycon']=='NO')])
            #minCSi = len(dfdtto[(dfdtto['Categoria']=='Ministro Cristiano') & (dfdtto['paycon']=='SI')])
            #minCPend = len(dfdtto[(dfdtto['Categoria']=='Ministro Cristiano') & (dfdtto['paycon']=='PENDIENTE')])
            #fila minD

            minDNo = dfdtto.loc[(df['Categoria'] == 'Ministro Distrital') & (dfdtto['paycon'] == 'NO')].shape[0]
            minDSi = dfdtto.loc[(df['Categoria'] == 'Ministro Distrital') & (dfdtto['paycon'] == 'SI')].shape[0]
            minDPend = dfdtto.loc[(df['Categoria'] == 'Ministro Distrital') & (dfdtto['paycon'] == 'PENDIENTE')].shape[0]

            #minDNo =dfdtto.loc[(dfdtto['Categoria'] == 'Ministro Distrital') & (dfdtto['paycon'] == 'NO'), ['Categoria', 'paycon']].apply(pd.Series.value_counts)
            #minDSi =dfdtto.loc[(dfdtto['Categoria'] == 'Ministro Distrital') & (dfdtto['paycon'] == 'SI'), ['Categoria', 'paycon']].apply(pd.Series.value_counts)
            #minDPend =dfdtto.loc[(dfdtto['Categoria'] == 'Ministro Distrital') & (dfdtto['paycon'] == 'PENDIENTE'), ['Categoria', 'paycon']].apply(pd.Series.value_counts)
            # minDNo = len(df[(df['Categoria']=='Ministro Distrital') & (df['paycon']=='NO')])
            # minDSi = len(df[(df['Categoria']=='Ministro Distrital') & (df['paycon']=='SI')])
            # minDPend = len(df[(df['Categoria']=='Ministro Distrital') & (df['paycon']=='PENDIENTE')])
            # fila minL

            minLNo = dfdtto.loc[(df['Categoria'] == 'Ministro Licenciado') & (dfdtto['paycon'] == 'NO')].shape[0]
            minLSi = dfdtto.loc[(df['Categoria'] == 'Ministro Licenciado') & (dfdtto['paycon'] == 'SI')].shape[0]
            minLPend = dfdtto.loc[(df['Categoria'] == 'Ministro Licenciado') & (dfdtto['paycon'] == 'PENDIENTE')].shape[0]

            #minLNo =dfdtto.loc[(dfdtto['Categoria'] == 'Ministro Licenciado') & (dfdtto['paycon'] == 'NO'), ['Categoria', 'paycon']].apply(pd.Series.value_counts)
            #minLSi =dfdtto.loc[(dfdtto['Categoria'] == 'Ministro Licenciado') & (dfdtto['paycon'] == 'SI'), ['Categoria', 'paycon']].apply(pd.Series.value_counts)
            #minLPend =dfdtto.loc[(dfdtto['Categoria'] == 'Ministro Licenciado') & (dfdtto['paycon'] == 'PENDIENTE'), ['Categoria', 'paycon']].apply(pd.Series.value_counts)
            #minLNo = len(dfdtto[(dfdtto['Categoria']=='Ministro Licenciado') & (dfdtto['paycon']=='NO')])
            #minLSi = len(dfdtto[(dfdtto['Categoria']=='Ministro Licenciado') & (dfdtto['paycon']=='SI')])
            #minLPend = len(dfdtto[(dfdtto['Categoria']=='Ministro Licenciado') & (dfdtto['paycon']=='PENDIENTE')])
            # minO

            minONo = dfdtto.loc[(df['Categoria'] == 'Ministro Ordenado') & (dfdtto['paycon'] == 'NO')].shape[0]
            minOSi = dfdtto.loc[(df['Categoria'] == 'Ministro Ordenado') & (dfdtto['paycon'] == 'SI')].shape[0]
            minOPend = dfdtto.loc[(df['Categoria'] == 'Ministro Ordenado') & (dfdtto['paycon'] == 'PENDIENTE')].shape[0]

            #minONo =dfdtto.loc[(dfdtto['Categoria'] == 'Ministro Ordenado') & (dfdtto['paycon'] == 'NO'), ['Categoria', 'paycon']].apply(pd.Series.value_counts)
            #minOSi =dfdtto.loc[(dfdtto['Categoria'] == 'Ministro Ordenado') & (dfdtto['paycon'] == 'SI'), ['Categoria', 'paycon']].apply(pd.Series.value_counts)
            #minOPend =dfdtto.loc[(dfdtto['Categoria'] == 'Ministro Ordenado') & (dfdtto['paycon'] == 'PENDIENTE'), ['Categoria', 'paycon']].apply(pd.Series.value_counts)
            
            #minONo = len(dfdtto[(dfdtto['Categoria']=='Ministro Ordenado') & (dfdtto['paycon']=='NO')])
            #minOSi = len(dfdtto[(dfdtto['Categoria']=='Ministro Ordenado') & (dfdtto['paycon']=='SI')])
            #minOPend = len(dfdtto[(dfdtto['Categoria']=='Ministro Ordenado') & (dfdtto['paycon']=='PENDIENTE')])
            #minC,minL,minO,minD2
            dftotXdtto = pd.DataFrame([(minC, minCNo, minCPend, minCSi),
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
            "yAxis": {"type": "category", "data": ['M. Cristiano', 'M.Distrital','M. Licenciado', 'M. Ordenado'],},
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
    df = df.reindex(columns=['Distrito', 'Categoria', 'cedula', 'Nombres', 'Apellidos', 'Email', 'Telefono', 'paycon', 'Modalidad', 'MontoApagar', 'montoPago', 'Diferencia', 'fuenteOrigen', 'referenciaPago', 'fechaPago'])
    st.dataframe(df.style.apply(row_style, axis=1))
    
regresar = st.button('Volver')
if regresar:
    switch_page('logmi')
st.page_link("pages/home2024.py", label="Inicio", icon="🏠")