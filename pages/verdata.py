
import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from deta import Deta

from PIL import Image

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')

logina = st.session_state['logina']
#logina
st.image(imagen1)
st.image(imagen2)

st.write('Hola ****' + logina['user'] + '****')
st.write('Aquí tienes la data del distrito: ****' + logina['Distrito'] + '****')
if logina['tipou']!='Admin':
    dtto = logina['Distrito']
else:
    dtto = ''
deta = Deta(st.secrets["deta_key"])
encprof = deta.Base('ProndanminFull01')
if dtto!='':
    db_content = encprof.fetch({'Distrito':dtto}).items
else:
    db_content = encprof.fetch().items
#st.write(db_content)
df = pd.DataFrame.from_dict(db_content)
df.rename(columns={"key": "cedula"}, inplace=True) # cambia el nombre de la columna KEY a CEDULA
df = df.reindex(columns=['cedula', 'Nombres', 'Apellidos','Categoria','Email','Telefono','Distrito','Modalidad','Status', 'ReporteCertif']) #Reordena las columnas como se mostraran


with st.expander('ver data'):
    df
regresar = st.button('Volver')
if regresar:
    switch_page('logmi')

#busq = pdwks.where(pdwks['Cédula de Identidad']='5125570')
#busq = pdwks[pdwks['Cédula de Identidad'].str.contains('5125570')]
#fibusq