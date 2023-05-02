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
pronda = deta.Base('ProndanminFull01')
drive = deta.Drive("minec")
dicPminec =  drive.list()

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
    ph1.subheader(' Cierre de participación en cursos PRONDAMIN2023')
    # ch_data = False
    cedula = ph1.text_input('Introduzca su número de cédula y/o documento de identidad :id:',key='iced',placeholder='ingrese su ID')
    try:
        buscado = pronda.get(cedula)
    except:
        if cedula=='':
            ph1.write('Ingrese numero de cedula o :id:')
        # else:
        #     ph1.write('cedula no existe')
        #     ph1.warning('''El número de cedula/id:id: NO aparece en nuestra base de datos.:file_cabinet:
                    # :arrow_right: Tendrá que registrarse nuevamente y al momento de hacerlo deberá introducir un requerimiento de revisión de data.
                    # Entonces procederemos a procesar su requerimiento y en un plazo:date: razonable le
                    # daremos una respuesta adecuada. Gracias por su paciencia, pero le recordamos
                    # que fue usted mismo quien inscribió sus datos en nuestra base de datos	:card_index:''')
            
    else:
        #ph1.write(first)
        if buscado!=None:
            cedmin = cedula
            status = buscado['Status']
            if status=='Aprobado':
                #ph1.write(buscado)
                ph1.success('**$\\large✨Felicitaciones✨$**  ministro :blue[**_' +buscado['Nombres']+' '+buscado['Apellidos'] + '_** ], $\\newline$ por haber realizado y aprobado el curso de : $\\newline$ :orange[**Ministro Ordenado - PRONDAMIN2023**].$\\newline$ Tu calificación final fue de :blue[20]')
                ph1.markdown('La temática del curso estudiado abarcó: $\\newline$ 🔹:violet[**Predicación Poderosa**], preparado por el Rvdo Wilmer Pérez $\\newline$ 🔹:violet[**Una  Nueva  Visión Y  Un  Nuevo  Comienzo**], preparado por el Rvdo Gregorio Acosta $\\newline$ 🔹:violet[**Llenura del Espíritu Santo en la Predicación**], preparado por el Rvdo Gregorio Acosta')
                ph1.success('👇👇**Aquí está tu certificado**.👇👇')
                buscaCerti = [imags for imags in dicPminec['names'] if cedula in imags]
                CertiEncontrado = buscaCerti[0]
                st.write(CertiEncontrado)
                imag = drive.get(CertiEncontrado)
                ph1.image(imag.read())

                btnd = ph1.button('descargar certificado')
                if btnd:
                    file = drive.get(CertiEncontrado)
                    with open(CertiEncontrado, "wb") as f:
                        f.write(file.read())
                    ph1.write('Certificado descargado!')
                correo = ph1.text_input(label='Enviar certificado a: ',placeholder=buscado['Email'])
                btnemail = ph1.button('enviar al correo')
                if btnemail:
                    file = drive.get(CertiEncontrado)
                    with open(CertiEncontrado, "wb") as f:
                        f.write(file.read())
                    send_email(certificado=CertiEncontrado, fromE='pjluis1010@gmail.com', toE=correo, clave='xlevnvykrkckojgs',asunto='Certificado Prondamin2023')


            else:
                #ph1.write(buscado)
                ph1.warning('Lo sentimos, todavía no apareces aprobado')
        else:
            #ph1.write('cedula no existe')
            ph1.error('''Lo sentimos, pero el número de cédula/:id: ingresado, **NO** aparece en nuestra base de datos:file_cabinet:. :arrow_right: :arrow_right: Por favor, intente nuevamente o comuníquese con el representante de **MINEC** en su distrito.
                    ''')
