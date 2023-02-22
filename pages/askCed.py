import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

urlcsv = 'https://raw.githubusercontent.com/pjluispb/miscvs/main/Prondanmin23.csv'
df = pd.read_csv(urlcsv, index_col='cedula')
#df = pd.read_csv("Prondanmin23.csv", index_col='cedula')
edo = 'inicial'
#b0 = st.button("b0")
#b1 = st.button("b1")
#st.write(edo)
def hide01():
        b0=False
        b1=True
        return
if edo=='inicial':
        b0=True
        b1=False
elif edo=='confirmar':
        b0=False
        b1=True
ch_data = False
if b0:
        with st.expander(label="Actualizar datos del ministro", expanded=True):
                ph1=st.container() 
                ph1.subheader(' Actualizar datos del ministro')
                # ch_data = False
                cedula = ph1.text_input('Número de cédula y/o documento de identidad :id:',key='iced')
                try:
                        first = df.loc[int(cedula)]
                except:
                        if cedula=='':
                                st.write('Ingrese un numero de cedula')
                        else:
                                st.write('cedula no existe')
                                st.warning('''El número de cedula/id:id: NO aparece en nuestra base de datos.:file_cabinet:
                                        :arrow_right: Tendrá que registrarse nuevamente y al momento de hacerlo deberá introducir un requerimiento de revisión de data.
                                        Entonces procederemos a procesar su requerimiento y en un plazo:date: razonable le
                                        daremos una respuesta adecuada. Gracias por su paciencia, pero le recordamos
                                        que fue usted mismo quien inscribió sus datos en nuestra base de datos	:card_index:''')
                                newRegB = st.button('Ir a nuevo registro :new:')
                                if newRegB:
                                        switch_page("newReg")
                else:
                        cedmin = cedula
                        ch_data = True
                        ph1.text('Los siguientes campos pueden ser actualizados')
                        nombres = ph1.text_input('Nombres :name_badge:', value = df.at[int(cedula),'Nombres'])
                        apellidos = ph1.text_input('Apellidos:',value = df.at[int(cedula),'Apellidos'])
                        correo = ph1.text_input('Correo Electrónico: 	:email:',value = df.at[int(cedula),'correo'])
                        telefono = ph1.text_input('Teléfono: :telephone_receiver:',value = df.at[int(cedula),'Teléfono'])
                        distrito = ph1.text_input('Distrito:',value = df.at[int(cedula),'Distrito'], disabled=True)
                        catasp = ph1.text_input('Categoría que aspira: :male-judge:',value = df.at[int(cedula),'catAsp'], disabled=True)
                        #status = ph1.text_input('Status: :goal_net:',value = df.at[int(cedula),'STATUS'], disabled=True)
                        #modo = ph1.text_input('Modalidad: ', value = df.at[int(cedula),'Modalidad'], disabled=True)
if ch_data:
        confirmar = st.radio('¿Confirma la edición de la data y su registro en el próximo curso de MINEC?',('SI','NO'), index=1, horizontal=True)
        if confirmar=='SI':
                edo='confirmar'
                #st.info('Actualizando Datos:  '+edo)
                hide01()
                b1=True
        else:    
                st.warning('Por favor confirme la edicion para proceder a la actualizacion:  ')

if b1:
        with st.expander("ESTOS SON LOS DATOS ACTUALIZADOS", expanded=True):
                b0=False
                #b0
                df.at[int(cedmin),'Nombres'] = nombres
                df.at[int(cedmin),'Apellidos'] = apellidos
                df.at[int(cedmin),'correo'] = correo
                df.at[int(cedula),'Teléfono'] = telefono
                first = df.loc[int(cedmin)]
                first
                df.to_csv("Prondanmin23.csv")
                #cedmin
                #nombres
                #apellidos
                #correo
                #telefono
        recomenzar = st.button('Recomenzar')
        if recomenzar:
                switch_page('reiniciar')
        
st.write('----------------')
regresar = st.button('Volver')
if regresar:
    switch_page('logmi')
