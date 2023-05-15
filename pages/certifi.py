import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from deta import Deta
from PIL import Image
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import re
from datetime import datetime

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')

deta = Deta(st.secrets["deta_key"])
pronda = deta.Base('PRONDAMIN2023-Final')
drive = deta.Drive("minec")
dicPminec =  drive.list()

st.set_page_config(
    page_title="Minec Reg App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def send_email(certificado, fromE, toE, clave, asunto):
    msg = MIMEMultipart()

    # setup the parameters of the message
    password = clave
    msg['From'] = fromE
    msg['To'] = toE
    msg['Subject'] = asunto

    # attach image to message body
    with open(certificado, 'rb') as f:
        img_data = f.read()
        image = MIMEImage(img_data, name=certificado)
        msg.attach(image)

    # send the message via the server SMTP connection
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()


with st.expander(label="Prondamin2023 - Cierre", expanded=True):
    ph1=st.container() 
    ph1.subheader(' Módulo de Cierre de cursos PRONDAMIN2023 ')
    # ch_data = False
    cedula = ph1.text_input('Introduzca su número de cédula y/o documento de identidad :id:',key='iced',placeholder='ingrese su ID')
    try:
        buscado = pronda.get(cedula)
    except:
        if cedula=='':
            ph1.write('Ingrese numero de cedula o :id:')
            
    else:
        if buscado!=None:
            #st.write(buscado)
            cedmin = cedula
            status = buscado['STATUS']
            if status=='APROBADO':
                ph1.success('**$\\large✨Felicitaciones✨\\newline$**  ministro :blue[** ' +buscado['NOMBRES']+' '+buscado['APELLIDOS'] + ' ** ], $\\newline$ por haber realizado y aprobado el curso de : $\\newline$ :orange[**'+buscado['CURSOREALIZADO']+' - PRONDAMIN2023**].$\\newline$ ')
                #ph1.markdown('La temática del curso estudiado abarcó: $\\newline$ 🔹:violet[**Predicación Poderosa**], preparado por el Rvdo Wilmer Pérez $\\newline$ 🔹:violet[**Una  Nueva  Visión Y  Un  Nuevo  Comienzo**], preparado por el Rvdo Gregorio Acosta $\\newline$ 🔹:violet[**Llenura del Espíritu Santo en la Predicación**], preparado por el Rvdo Gregorio Acosta')
                ph1.success('👇👇**Aquí está tu certificado**.👇👇')
                nombre = buscado['NOMBRES'] + ' ' + buscado['APELLIDOS']
                nnombre = nombre.replace(' ','')
                nnyced = nnombre+str(buscado['CEDULA'])+'.png'
                imag = drive.get(nnyced)
                ph1.image(imag.read())
                
                ph1.success('Para :red[**guardar**] la 👆imagen👆 de tu certificado👆 en tu :orange[**computadora**]💻, _puedes hacer clic con el **botón derecho** sobre la 👆imagen👆, y elegir en el **menú contextual** la opción de :blue[**imprimir**]🖨️ ó :blue[**guardar imagen como**]_.📂 $\\newline$ En caso de que lo hagas desde una :orange[**tablet o un celular**]📱, manten la imagen _presionada_ y te aparecerá un **_menú contextual_** con las opciones de :blue[**agregar a fotos**]🖼️ (_se descargará en la carpeta :red[**Fotos**] de tu dispositivo_), :blue[**compartir**]✉️ (_que te permitirá enviarlo a un correo electrónico, Whatsapp, Telegram, Drive, etc_) y la de :blue[**copiar**] (_copia la imagen en memoria para pegarlo en otra aplicación tal como Powerpoint, Notas, etc_)')
                #correo = ph1.text_input(label='Enviar certificado a: ',placeholder=buscado['EMAIL'],)
                #btnemail = ph1.button('enviar al correo')
                #if btnemail:
                #    file = drive.get(nnyced)
                #    with open(nnyced, "wb") as f:
                #        f.write(file.read())
                    #send_email(certificado=nnyced, fromE='pjluis1010@gmail.com', toE=correo, clave='xlevnvykrkckojgs',asunto='Certificado Prondamin2023')
            else:
                ph1.warning(' _Estimado ministr@_: ↔️:red[ **'+buscado['NOMBRES']+' '+buscado['APELLIDOS']+ '** ], sentimos que no haya podido aprobar el curso de ' + buscado['CURSOREALIZADO']+'. ➡️➡️➡️Tendrá que volver a realizarlo el próximo año')
        else:
            #ph1.write('cedula no existe')
            ph1.error('''Lo sentimos, pero el número de cédula/:id: ingresado, **NO** aparece en nuestra base de datos:file_cabinet:. :arrow_right: :arrow_right: Por favor, intente nuevamente o comuníquese con el representante de **MINEC** en su distrito.
                    ''')
