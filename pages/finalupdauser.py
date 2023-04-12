
import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from deta import Deta
from PIL import Image
import re
from datetime import datetime

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')
st.image(imagen1)
st.image(imagen2)

deta = Deta(st.secrets["deta_key"])
prondadb = deta.Base('ProndanminFull01')
cedula = st.session_state['cedula']
#cedula
pronda = prondadb.fetch(limit=5000)
dfpron = pd.DataFrame(pronda.items)
dfcedula = dfpron[dfpron['key']==cedula]
#st.write(dfcedula)
registro = dfcedula.to_dict('dict')
#registro
rcedula = list(dfcedula['key'].items())[0][1]
rnombre = list(dfcedula['Nombres'].items())[0][1]
rapellido = list(dfcedula['Apellidos'].items())[0][1]
rcorreo = list(dfcedula['correo'].items())[0][1]
rtelefono = list(dfcedula['Telefono'].items())[0][1]
rdtto = list(dfcedula['Distrito'].items())[0][1]
rcatmi = list(dfcedula['Categoria'].items())[0][1]

coordimdb = deta.Base('coordi-minec')
coordina = coordimdb.fetch({'Distrito':rdtto})
#coordina.items
coordinadorDtto = coordina.items[0]['Nombre']
coordinadorTelf = coordina.items[0]['telefono']

rpaycon = list(dfcedula['paycon'].items())[0][1]
rmontoApagar = list(dfcedula['MontoApagar'].items())[0][1]
rmodo = list(dfcedula['Modalidad'].items())[0][1]
rfechapago = list(dfcedula['fechaPago'].items())[0][1]
rfuenteorigen = list(dfcedula['fuenteOrigen'].items())[0][1]
rmontopago = list(dfcedula['montoPago'].items())[0][1]
rReferenciaPago = list(dfcedula['referenciaPago'].items())[0][1]
st.title('Bienvenido a :blue[PRONDAMIN 2023]')
st.subheader('Gracias ministro :red['+rnombre+' '+rapellido+ '], por actualizar sus datos')

st.subheader('Su matriculación ha sido recibida con éxito:heavy_check_mark:')
st.subheader('Muy pronto :hourglass: será procesada.')

st.markdown(' Contacte al coordinador de Educación Cristiana de su distrito :blue[**'+rdtto+'**]:')
st.markdown(' :blue[Rvdo. '+'**'+coordinadorDtto+'**]  '+'  :telephone_receiver:   Teléfono : '+':red[**'+coordinadorTelf+'**]')
st.markdown('Te invitamos a unirte a un grupo: https://chat.whatsapp.com/KmDnXJp1CF23mXe4cU3GEG')
st.write('---')
st.write('')
st.write('')
if rpaycon=='NO':
    st.error('Aún no se ha inscrito en PRONDANMIN. Le animamos a realizarlo pronto.')
    tmsg = 1
    msg='Animo!! Inscríbase YA \n No pierda la oportunidad de actualizar su categoría ministerial'
elif rpaycon=='PENDIENTE':
    st.warning(':eye-in-speech-bubble:   Su pago(#ref: :blue['+ rReferenciaPago +']) ha sido **registrado** y será 	:ballot_box_with_check:**confirmado** a la brevedad posible por nuestro :green[_departamento de finanzas_]')
    tmsg = 2

elif rpaycon=='PENDIENTE x DIFERENCIA':
    st.error('Su pago fue registrado y confirmado, pero es insuficiente para cubrir la inscripción en PRONDANMIN. Por favor realice otro pago para completar el monto del registro en el curso.')
    tmsg = 2
    msg='----'
else: 
    st.success('Pago realizado, confirmado y completo. Está listo para comenzar el curso PRONDANMIN')
    tmsg = 3

if tmsg==1: st.subheader(msg)

salir = st.button('Salir')
if salir:
    switch_page('reinicia02')
st.write('---')
