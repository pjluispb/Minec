import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from deta import Deta
from PIL import Image
import re
from datetime import datetime


def is_number(string):
    regex = r"^\d+(\.\d{1,2})?$"
    return bool(re.match(regex, string))

def is_valid_date(string):
    try:
        date = datetime.strptime(string, "%d/%m/%y")
        return date.day in range(1, 32) and date.month in range(1, 13) and date.year == 2023
    except ValueError:
        return False
    
def is_valid_email(string):
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(regex, string))


imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')

deta = Deta(st.secrets["deta_key"])
encprof = deta.Base('ProndanminFull01')
montopay = deta.Base('MontoAPagar')
montoApagar = montopay.fetch()
#logina = st.session_state['logina']
#logina
st.image(imagen1)
st.image(imagen2)

edo = 'inicial'
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
        with st.expander(label="-", expanded=True):
                ph1=st.container() 
                ph1.subheader(' Bienvenido ministro a la aplicación de registro en cursos de la MINEC')
                # ch_data = False
                cedula = ph1.text_input('Introduzca su número de cédula y/o documento de identidad :id: para comenzar',key='iced',placeholder='ingrese su ID')
                try:
                        first = encprof.get(cedula)
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
                        #ph1.write(first)
                        if first!=None:
                                cedmin = cedula
                                ch_data = True
                                sherr = False
                                ph1.text('Edite los siguientes campos')
                                nombres = ph1.text_input('Nombres :name_badge:', value = first['Nombres'])
                                apellidos = ph1.text_input('Apellidos:',value = first['Apellidos'])
                                correo = ph1.text_input('Correo Electrónico: 	:email:',value = first['Email'])
                                telefono = ph1.text_input('Teléfono: :telephone_receiver:',value = first['Telefono'])
                                distrito = ph1.text_input('Distrito:',value = first['Distrito'], disabled=True)
                                catasp = ph1.text_input('Categoría: :male-judge: _(Esta información proviene de los registros de cada distrito)_',value = first['Categoria'], disabled=True)
                                ph1.write('---')
                                ph1.write('Datos acerca del pago')
                                modalidad = ph1.radio(label='Modalidad del curso', options=['Virtual', 'Presencial'], horizontal=True)
                                if modalidad=='Virtual': montoAcancelar = montoApagar.items[0]['MontoAPagarVirtual']
                                else: montoAcancelar = montoApagar.items[0]['MontoAPagarPresencial']
                                if first['paycon'] == 'SI': valpay = True
                                else: 
                                        valpay = False
                                        ph1.write('➡️➡️➡️➡️ _Monto a cancelar por modalidad_   ↔️:red[ **'+ modalidad+ ': Bs '+montoAcancelar+'** ]')
                                pagoConfirmado = ph1.text_input('Pago Confirmado', value = first['paycon'], disabled = True)
                                #fuenteOrigen = ph1.text_input('Origen del pago(Transferencia, Pago Movil)', value = first['fuenteOrigen'], disabled = valpay)
                                fuenteOrigen = ph1.radio('Origen del pago(Transferencia o Pago Movil) :red[**:eyes: OJO:eyes: debe seleccionar una opción:arrow_lower_left: para continuar e ingresar o editar los datos de pago**]', options=['','Pago Movil', 'Transferencia'],horizontal=True)
                                if fuenteOrigen != '': sherr = True
                                fechaPago = ph1.text_input('Fecha de pago _(dd/mm/aa)_', value = first['fechaPago'], disabled = not(sherr))
                                if not(is_valid_date(fechaPago)):
                                       if sherr:
                                            st.error('Error: El formato de la fecha debe ser dd/mm/aa y el año 23')

                                referenciaPago = ph1.text_input('Nro de referencia del pago (últimos 4 dígitos)', value = first['referenciaPago'], disabled = not(sherr))
                                if not(len(referenciaPago)==4 and referenciaPago.isalnum()):
                                        if sherr:
                                            st.error('Error: El Nro de referencia del pago debe contener solo 4 dígitos')
                                
                                montoPago = ph1.text_input('Monto pagado', value = first['montoPago'], disabled = not(sherr))
                                if not(is_number(montoPago)):
                                        if sherr:
                                            st.error('Error: el monto pago debe ser un número válido. Sólo dígitos y punto(.) decimal')

                        else:
                                st.warning('El número de documento de identidad:id: ingresado **NO** aparece en nuestra base de datos.:file_cabinet: :arrow_right: intente de nuevo, y si luego de varios intentos no aparece su información, entonces tendrá que ponerse de acuerdo con el representante de MINEC de su distrito')
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
                if first['paycon']=='SI':  newpaycon = 'SI'
                elif first['paycon']=='NO': 
                        if (fuenteOrigen != '-') or (referenciaPago != '-') or (montoPago != '-') or (fechaPago != '-'): 
                                newpaycon = 'PENDIENTE'
                        else:   
                                newpaycon = 'NO'
                                fuenteOrigen, referenciaPago = '-', '-'
                                montoPago, fechaPago = '-', '-'
                else : newpaycon = 'PENDIENTE'

                updates = {'Nombres': nombres,
                           'Apellidos': apellidos,
                           'Email': correo,
                           'Telefono': telefono,
                           'paycon': newpaycon,
                           'fuenteOrigen': fuenteOrigen,
                           'fechaPago': fechaPago,
                           'referenciaPago': referenciaPago,
                           'montoPago': montoPago,
                           'MontoApagar': montoAcancelar,
                           'Modalidad': modalidad}
                #updates, cedula

                encprof.update(updates, cedula)
                registro = encprof.get(cedula)
                st.write('Sus datos han sido actualizados y a continuacion se muestra como quedaron guardados')
                col1, col2 = st.columns(2)
                with col1:
                        st.info('Cédula o documento de identificación : ')
                        st.write('**Nombres**')
                        st.success(registro['Nombres'], icon="📛")
                        st.write('**Correo electronico**')
                        st.info(registro['Email'], icon="✉️")
                        st.write('**Modalidad**')
                        st.success(registro['Modalidad'], icon="🖥️")
                        st.write('**Origen (Transferencia, Pago Movil)**')
                        st.info(registro['fuenteOrigen'], icon="💳")
                        st.write('**Nro de referencia del pago (últimos 4 dígitos)**')
                        st.success(registro['referenciaPago'], icon="🔢")
                with col2:
                        st.success(registro['key'], icon="ℹ️")
                        st.write('**Apellidos**')
                        st.info(registro['Apellidos'], icon="ℹ️")
                        st.write('**Teléfono**')
                        st.success(registro['Telefono'], icon="📞")
                        st.write('**Monto A Cancelar**')
                        st.info(registro['MontoApagar'], icon="💴")
                        st.write('**Fecha de Pago**')
                        st.success(registro['fechaPago'], icon="📆")
                        st.write('**Monto de Pago**')
                        st.info(registro['montoPago'], icon="💴")
                        

                # #df.to_csv("Prondanmin23.csv")
                # df.to_csv(urlcsv)
                
        recomenzar = st.button('Finalizar')
        if recomenzar:
                #cedula = ''
                st.session_state['cedula'] = cedula
                switch_page('finalupdauser')
        
st.write('----------------')
# regresar = st.button('Volver a Principal')
# if regresar:
#     switch_page('logmi')
