import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

urlcsv = 'https://raw.githubusercontent.com/pjluispb/miscvs/main/Prondanmin23.csv'
df = pd.read_csv(urlcsv, index_col='cedula')
#df = pd.read_csv("Prondanmin23.csv", index_col='cedula')

st.title('Nuevo Registro')
ph1 = st.container()
with st.form('nuevo registro'):
    cedula = st.text_input('Cédula de identidad y/o documento de identidad :id:')
    nombres = st.text_input('Nombres: :name_badge:')
    apellidos = st.text_input('Apellidos:')
    correo = st.text_input('Correo Electrónico: 	:email:')
    telefono = st.text_input('Teléfono: :telephone_receiver:')
    distrito = st.selectbox('Distrito:',['Andino','Centro','Centro Llanos', 'Falcón','Lara', 'Llanos','Llanos Occidentales','Metropolitano','Nor Oriente','Sur Oriente','Yaracuy','Zulia'])
    #distrito = st.radio('Distrito:',['Andino','Centro','Centro Llanos', 'Falcón','Lara', 'Llanos','Llanos Occidentales','Metropolitano','Nor Oriente','Sur Oriente','Yaracuy','Zulia'], horizontal=True)
    #observacion = st.text_area('ingrese requerimiento de revision', value='ninguna')
    registrar = st.form_submit_button('registrar nueva entrada')
    if registrar:
        categoria, modalidad, status, observacion = 'S/A', 'S/A', 'S/A', 'S/A'
        entradas = ['55',correo,apellidos,nombres,cedula,telefono,distrito,categoria,modalidad,status,observacion]
        if '' in entradas:
            ph1.warning('Debe llenar todos los campos')
        else:                 # Agrega fila al df
            index_name=int(cedula)
            new_indexes = df.index.insert(1, index_name) 
            newRow = pd.Series({'correo':correo,'Apellidos':apellidos,'Nombres':nombres,'Teléfono':telefono,'Distrito':distrito,'catAsp':'S/A','modalidad':'S/A','STATUS':'S/A'}, name=index_name)
            #st.write(newRow,ignore_index=True)
            df_new_row = pd.DataFrame([newRow], columns=df.columns) 
            df = pd.concat([df, df_new_row]) 
            df.to_csv(urlcsv , encoding='utf-8', index=True, index_label='cedula') 
            st.success('Registro agregado a la base de datos')
            reg = df.loc[int(cedula)]
            reg
regresar = st.button('Volver')
if regresar:
    switch_page('logmi')
