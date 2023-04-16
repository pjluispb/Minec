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
pagocomp = deta.Base('PagoRegistrados')
#logina = st.session_state['logina']
#logina
st.image(imagen1)
st.image(imagen2)

switch_page("deshabilitado")

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
                                if first['paycon']=='NO' or first['paycon']=='PENDIENTE':
                                        if first['paycon']=='PENDIENTE':
                                                ph1.warning(':red[**ATENCION:**] Su :blue[**pago**] ha sido **_registrado_** pero :red[**NO** se ha confirmado] aún. Si desea, a continuación puede cambiar alguna información del pago o de los datos personales')
                                                permitirModalidad = False
                                                permitirEditarPago = False
                                                primeravez = False
                                        else: 
                                                permitirModalidad = True
                                                permitirEditarPago = True
                                                primeravez = True
                                        permitirModalidad = True
                                        ch_data = True
                                        sherr = False
                                        errores = False
                                        ph1.text('Edite/Actualice los siguientes campos')

                                        nombres = ph1.text_input('Nombres :name_badge:', value = first['Nombres'])
                                        apellidos = ph1.text_input('Apellidos:',value = first['Apellidos'])
                                        try:
                                            first['Email']
                                        except:
                                            first['Email']='-'    
                                        correo = ph1.text_input('Correo Electrónico: 	:email:',value = first['Email'])
                                        # if not(is_valid_email(correo)):
                                        #        st.error('Error: El formato del correo debe ser similar a: xxxxx@yyyy.zzz')
                                        #        errores = True
                                        try:
                                            first['Telefono']
                                        except:
                                            first['Telefono']='-' 
                                        telefono = ph1.text_input('Teléfono: :telephone_receiver:',value = first['Telefono'])
                                        distrito = ph1.text_input('Distrito:',value = first['Distrito'], disabled=True)
                                        catasp = ph1.text_input('Categoría Ministerial: :male-judge:',value = first['Categoria'], disabled=True)
                                        ph1.write('---')
                                        ph1.write('Datos acerca del pago')
                                        #if permitirModalidad:
                                        if first['Modalidad']=='Virtual':indexrMO=0
                                        else: indexrMO=1
                                        modalidad = ph1.radio(label='Modalidad del curso', options=['Virtual', 'Presencial'], horizontal=True)
                                        if modalidad=='Virtual': 
                                                montoAcancelarEdi = montoApagar.items[0]['MontoAPagarVirtual']
                                                if not(is_valid_email(correo)):
                                                        st.error('Error: La modalidad Virtual implica tener un correo válido, con un formato similar a: xxxxx@yyyy.zzz')
                                                        errores = True
                                        else: montoAcancelarEdi = montoApagar.items[0]['MontoAPagarPresencial']

                                        montoAcancelar = ph1.text_input(label='Monto a pagar', value=montoAcancelarEdi, disabled=True)
                                        # else:
                                        #         modalidad = ph1.text_input(label='Modalidad:', value=first['Modalidad'], disabled=True)
                                        #         montoAcancelar = ph1.text_input(label='Monto a pagar', value=first['MontoApagar'], disabled=True)
                                        
                                        #ph1.write(permitirModalidad)

                                        # if first['paycon'] == 'SI': valpay = True
                                        # else: 
                                        #         valpay = False
                                        #         ph1.write('➡️➡️➡️➡️ _Monto a cancelar por modalidad_   ↔️:red[ **'+ modalidad+ ': Bs '+montoAcancelar+'** ]')
                                        
                                        # if first['paycon'] == 'SI': valpay = True
                                        # else: valpay = False
                                        pagoConfirmado = ph1.text_input('Status del Pago ', value = first['paycon'], disabled = True)
                                        #ph1.write(primeravez)
                                        if not(primeravez):
                                                SiEditarPago = ph1.radio('Desea editar el pago?', options=['SI', 'NO'], horizontal=True, index=1)
                                                if SiEditarPago=='SI': permitirEditarPago=True
                                        if permitirEditarPago:
                                                #ph1.write(first)
                                                try:
                                                    if first['fuenteOrigen']=='Pago Movil': indexrFO=0
                                                    else: indexrFO=1
                                                except:
                                                    indexrFO=0
                                               
                                                fuenteOrigen = ph1.radio('Origen del pago(Transferencia o Pago Movil) : ', options=['Pago Movil', 'Transferencia'],horizontal=True, index=indexrFO)
                                                if fuenteOrigen != '': sherr = True
                                        else: fuenteOrigen = ph1.text_input(label='Origen del pago', value=first['fuenteOrigen'],disabled=True)
                                        try:
                                            first['fechaPago']
                                        except:
                                            first['fechaPago']='-'

                                        fechaPago = ph1.text_input('Fecha de pago (dd/mm/aa)', value = first['fechaPago'], disabled = not(sherr))
                                        if not(is_valid_date(fechaPago)):
                                                if sherr:
                                                        st.error('Error: El formato de la fecha debe ser dd/mm/aa y el año 23')
                                                        errores = True
                                        try:
                                            first['referenciaPago']
                                        except:
                                            first['referenciaPago']='-'

                                        referenciaPago = ph1.text_input('Nro de referencia del pago (últimos 4 dígitos)', value = first['referenciaPago'], disabled = not(sherr))
                                        if not(len(referenciaPago)==4 and referenciaPago.isalnum()):
                                                if sherr:
                                                        st.error('Error: El Nro de referencia del pago debe contener solo 4 dígitos')
                                                        errores = True
                                        try:
                                            first['montoPago']
                                        except:
                                            first['montoPago']='-'
                                        montoPago = ph1.text_input('Monto pagado', value = first['montoPago'], disabled = not(sherr))
                                        if not(is_number(montoPago)):
                                                if sherr:
                                                        st.error('Error: el monto pago debe ser un número válido. Sólo dígitos y punto(.) decimal')
                                                        errores = True
                                                

                                elif first['paycon']=='SI':
                                        #st.write('paycon = '+first['paycon']+'...procedimiento de mostrar reg completado')
                                        #st.write('muestra los datos personales y los de pago...solo puede editar los personales(N-A-T-C)')
                                        ph1.success(':blue[**ATENCION:**] Su :blue[**pago**] ha sido **_registrado_** y :blue[**confirmado**]. Si desea, a continuación puede cambiar alguna información sobre sus datos personales')
                                        ch_data = True
                                        sherr = False
                                        errores = False
                                        ph1.text('Edite/Actualice los siguientes campos')
                                        nombres = ph1.text_input('Nombres :name_badge:', value = first['Nombres'])
                                        apellidos = ph1.text_input('Apellidos:',value = first['Apellidos'])
                                        correo = ph1.text_input('Correo Electrónico: 	:email:',value = first['Email'])
                                        if not(is_valid_email(correo)):
                                               st.error('Error: El formato del correo debe ser similar a: xxxxx@yyyy.zzz')
                                               errores = True
                                        telefono = ph1.text_input('Teléfono: :telephone_receiver:',value = first['Telefono'])
                                        distrito = ph1.text_input('Distrito:',value = first['Distrito'], disabled=True)
                                        catasp = ph1.text_input('Categoría Ministerial: :male-judge:',value = first['Categoria'], disabled=True)
                                        ph1.write('---')
                                        ph1.write('Datos acerca del pago')
                                        ph1.info('Modalidad : :green[**' + first['Modalidad'] + '**]')
                                        ph1.success('Nro de referencia del pago : :orange[**' + first['referenciaPago']+'**]', icon="🔢")
                                        ph1.info('Modo de pago: :green[**' +first['fuenteOrigen']+'**]', icon="💳")
                                        ph1.success('Monto de Pago: :orange[**'+first['montoPago']+'**]', icon="💴")
                                        ph1.info('Fecha de Pago: :green[**'+first['fechaPago']+'**]', icon="📆")
                                           
                                elif first['paycon']=='SI++':
                                        #st.write('paycon = '+first['paycon']+'...procedimiento para pagos fraccionarios')
                                        #st.write('muestra los datos personales y los de pago...solo puede editar los personales(N-A-T-C) y agregar si el pago fraccionario(el exceso), se usará para abonar el pago de otro usuario(debe dar la cedula de dicho usuario) o se ofrendará a la Minec')
                                        ph1.success(':blue[**ATENCION:**] Su :blue[**pago**] ha sido **_registrado_** y :blue[**confirmado**]. Si desea, a continuación puede cambiar alguna información sobre sus datos personales y además puede decirnos en que se usará el monto excedente, el cuál puede ser ofrendado al ministerio de MINEC ó usado como abono para el curso PRONDANMIN de otro ministro')
                                        ch_data = True
                                        sherr = False
                                        errores = False
                                        ph1.text('Edite/Actualice los siguientes campos')
                                        nombres = ph1.text_input('Nombres :name_badge:', value = first['Nombres'])
                                        apellidos = ph1.text_input('Apellidos:',value = first['Apellidos'])
                                        correo = ph1.text_input('Correo Electrónico: 	:email:',value = first['Email'])
                                        if not(is_valid_email(correo)):
                                               st.error('Error: El formato del correo debe ser similar a: xxxxx@yyyy.zzz')
                                               errores = True
                                        telefono = ph1.text_input('Teléfono: :telephone_receiver:',value = first['Telefono'])
                                        distrito = ph1.text_input('Distrito:',value = first['Distrito'], disabled=True)
                                        catasp = ph1.text_input('Categoría Ministerial: :male-judge:',value = first['Categoria'], disabled=True)
                                        ph1.write('---')
                                        ph1.write('Datos acerca del pago')
                                        ph1.info('Modalidad : :green[**' + first['Modalidad'] + '**]')
                                        ph1.success('Nro de referencia del pago : :orange[**' + first['referenciaPago']+'**]', icon="🔢")
                                        ph1.info('Modo de pago: :green[**' +first['fuenteOrigen']+'**]', icon="💳")
                                        ph1.success('Monto de Pago: :orange[**'+first['montoPago']+'**]', icon="💴")
                                        ph1.info('Fecha de Pago: :green[**'+first['fechaPago']+'**]', icon="📆")
                                        ph1.write('---')
                                        ph1.success('Su pago supera el monto del curso registrado. Debe contactar al departamento de Finanzas de MINEC para ver que se hará  con la cantidad excedente')
                                        
                                elif first['paycon']=="PENDIENTE x DIFERENCIA":
                                        #st.write('paycon = '+first['paycon']+'...proc para cuando es necesario pagos complementarios')
                                        #st.write('muestra los datos personales y los de pago...puede editar los personales(N-A-T-C) y agregar nuevos datos de pago complementario')
                                        ph1.error(':orange[**ATENCION:**] Su :blue[**pago**] ha sido **_registrado_** y :blue[**confirmado**], pero es :red[**insuficiente**] para cubrir el monto del registro. Si lo desea, a continuación puede agregar un pago adicional y también cambiar alguna información sobre sus datos personales')
                                        ch_data = True
                                        sherr = False
                                        errores = False
                                        ph1.text('Edite/Actualice los siguientes campos')
                                        nombres = ph1.text_input('Nombres :name_badge:', value = first['Nombres'])
                                        apellidos = ph1.text_input('Apellidos:',value = first['Apellidos'])
                                        correo = ph1.text_input('Correo Electrónico: 	:email:',value = first['Email'])
                                        if not(is_valid_email(correo)):
                                               st.error('Error: El formato del correo debe ser similar a: xxxxx@yyyy.zzz')
                                               errores = True
                                        telefono = ph1.text_input('Teléfono: :telephone_receiver:',value = first['Telefono'])
                                        distrito = ph1.text_input('Distrito:',value = first['Distrito'], disabled=True)
                                        catasp = ph1.text_input('Categoría Ministerial: :male-judge:',value = first['Categoria'], disabled=True)
                                        ph1.write('---')
                                        # ph1.write('Datos acerca del pago ya registrado y confirmado')
                                        # ph1.info('Modalidad : :green[**' + first['Modalidad'] + '**]'+'◀️➖➖➖ ▶️  Total a cancelar: :green['+first['MontoApagar']+']')
                                        # #ph1.success('Nro de referencia del pago : :orange[**' + first['referenciaPago']+'**]', icon="🔢")
                                        # ph1.success('💳Modo de pago: :green[**' +first['fuenteOrigen']+'**]'+'◀️➖➖➖▶️'+'Nro de referencia del pago : :orange[**' + first['referenciaPago']+'**]🔢')
                                        # ph1.info('Monto de Pago: :orange[**'+first['montoPago']+'**]💴'+'◀️➖➖➖▶️'+'Fecha de Pago: :green[**'+first['fechaPago']+'**]📆')
                                        # #ph1.info('Fecha de Pago: :green[**'+first['fechaPago']+'**]', icon="📆")
                                        # ph1.write('---')
                                        #--------------------------------------------------
                                        ph1.subheader('Pagos Realizados')
                                        pagoIni = {'ID':first['key'],'confirmacion':first['paycon'], 'fecha':first['fechaPago'],'key':first['key']+'-'+first['referenciaPago'],'modoPago':first['fuenteOrigen'],'monto':first['montoPago'], 'referencia':first['referenciaPago'],'tipoPago':'Inicial'}
                                        pagoscom = pagocomp.fetch({'key?pfx':str(cedula)})
                                        if pagoscom.count>=1:
                                                pagosComRealizados = pagoscom.items
                                        lisPagos = []
                                        lisPagos.append(pagoIni)
                                        for pags in pagoscom.items:
                                                lisPagos.append(pags)
                                        dflisP = pd.DataFrame(lisPagos)
                                        #dflisP.rename(columns={'ID':'ID/Cédula'}, inplace=True)
                                        #dflisP.reindex(columns=['ID/Cédula','modoPago','confirmacion','fecha','monto','referencia','tipoPago'])
                                        #df4 = dflisP.T
                                        df4 = dflisP.transpose()
                                        df4 = df4.rename(index={0: 'row1', 1: 'row2', 2: 'row3'})
                                        #df4.rename(row={'ID':'ID/Cédula:id:'})
                                        #df4.rename(index={'ID':'ID/Cédula'})
                                        ph1.dataframe(df4)
                                        nroPagosRealizados = df4.shape[1]
                                        confVal = df4.loc['confirmacion'].values.tolist()
                                        coutPENDIENTEs = 0
                                        for x in confVal:
                                                if x.startswith('PENDIENTE'): coutPENDIENTEs+=1
                                        
                                        #ph1.write(confVal)
                                        #ph1.write((nroPagosRealizados))
                                        #-------------------------------------------
                                        NuevoPagoComp = ph1.radio(label='Desea realizar un nuevo pago?', options=['SI','NO'], index=1)
                                        if NuevoPagoComp=='SI':
                                                if nroPagosRealizados<=2 and coutPENDIENTEs<2:
                                                        pagoAdicional=True
                                                        ph1.subheader('Datos acerca del pago complementario/adicional')
                                                        # ph1.write(type(first['Diferencia']))
                                                        if first['Diferencia']!=' ':
                                                                diferencia = ph1.warning('Debe un diferencia de Bs.: :blue[' +str(first['Diferencia'])+']')
                                                        else:   
                                                                dife = float(first['MontoApagar'])-float(first['montoPago'])
                                                                # ph1.write(dife)
                                                                diferencia = ph1.warning('Debe un diferencia de Bs.: :blue[' +str(dife)+']')
                                                        
                                                        fuenteOrigenComp = ph1.radio('Origen del pago(Transferencia o Pago Movil) : ', options=['Pago Movil', 'Transferencia'],horizontal=True, index=0)
                                                        if fuenteOrigenComp != '': sherr = True
                                                        else: fuenteOrigenComp = ph1.text_input(label='Origen del pago', disabled=True)

                                                        referenciaPagoComp = ph1.text_input('Nro de referencia del pago (últimos 4 dígitos)', disabled = not(sherr))
                                                        if not(len(referenciaPagoComp)==4 and referenciaPagoComp.isalnum()):
                                                                if sherr:
                                                                        st.error('Error: El Nro de referencia del pago debe contener solo 4 dígitos')
                                                                        errores = True
                                                        
                                                        montoPagoComp = ph1.text_input('Monto',  disabled = not(sherr))
                                                        if not(is_number(montoPagoComp)):
                                                                if sherr:
                                                                        st.error('Error: el monto pago debe ser un número válido. Sólo dígitos y punto(.) decimal')
                                                                        errores = True
                                                        fechaPagoComp = ph1.text_input('Fecha de pago (dd/mm/aa)',  disabled = not(sherr))
                                                        if not(is_valid_date(fechaPagoComp)):
                                                                if sherr:
                                                                        st.error('Error: El formato de la fecha debe ser dd/mm/aa y el año 23')
                                                                        errores = True
                                                else:
                                                        ph1.error('No se puede registrar otro Pago Adicional hasta que no se confirmen los pagos anteriores. Por favor inténtelo más tarde ')
                                                        pagoAdicional=False


                                
                                else:
                                        st.write('No hay otra condición ...por ahora')

                        else:
                                st.warning('El número de documento de identidad:id: ingresado **NO** aparece en nuestra base de datos.:file_cabinet: :arrow_right: intente de nuevo, y si luego de varios intentos no aparece su información, entonces tendrá que ponerse de acuerdo con el representante de MINEC de su distrito')
if ch_data:
        confirmar = st.radio('¿Confirma la edición de la data y su registro en el próximo curso de MINEC?',('SI','NO'), index=1, horizontal=True)
        if confirmar=='SI' and not(errores):
                edo='confirmar'
                #st.info('Actualizando Datos:  '+edo)
                hide01()
                b1=True
        else:    
                if errores:
                       st.warning('Corrija los errores que hay en el formulario para poder continuar')
                else: 
                        st.warning('Por favor confirme la edicion para proceder a la actualizacion:  ')

if b1:
        with st.expander("ESTOS SON LOS DATOS ACTUALIZADOS", expanded=True):
                
                b0=False
                #st.write(first['paycon'])
                if first['paycon']=='SI':  
                        newpaycon = 'SI'
                        updates = {'Nombres': nombres,
                           'Apellidos': apellidos,
                           'Email': correo,
                           'Telefono': telefono}
                elif first['paycon']=='SI++':
                        newpaycon = 'SI++'
                        updates = {'Nombres': nombres,
                           'Apellidos': apellidos,
                           'Email': correo,
                           'Telefono': telefono}
                        # registro de asignacion de excedente
                elif first['paycon']=='PENDIENTE x DIFERENCIA':
                        newpaycon = 'PENDIENTE x DIFERENCIA'
                        updates = {'Nombres': nombres,
                           'Apellidos': apellidos,
                           'Email': correo,
                           'Telefono': telefono}
                        if pagoAdicional:
                                regPagoCom = {'ID': cedula,
                                      'key': cedula+'-'+referenciaPagoComp,
                                      'tipoPago':'Complementario',
                                      'modoPago': fuenteOrigenComp,
                                      'referencia':referenciaPagoComp,
                                      'monto':montoPagoComp,
                                      'fecha':fechaPagoComp,
                                      'confirmacion':'PENDIENTE'}
                        #pagocomp.put(regPagoCom)
                        #st.write('updates = ',updates)
                        # registro de pago complementario
                elif first['paycon']=='NO': 
                        if (fuenteOrigen != '-') or (referenciaPago != '-') or (montoPago != '-') or (fechaPago != '-'): 
                                newpaycon = 'PENDIENTE'
                                updates = {'Nombres': nombres,
                                        'Apellidos': apellidos,
                                        'correo': correo,
                                        'Telefono': telefono,
                                        'paycon': newpaycon,
                                        'Modalidad': modalidad,
                                        'MontoApagar': montoAcancelar,
                                        'fuenteOrigen': fuenteOrigen,
                                        'fechaPago': fechaPago,
                                        'referenciaPago': referenciaPago,
                                        'montoPago': montoPago}
                                
                        else:   
                                newpaycon = 'NO'
                                fuenteOrigen, referenciaPago = '-', '-'
                                montoPago, fechaPago = '-', '-'
                                updates = {'Nombres': nombres,
                                        'Apellidos': apellidos,
                                        'Email': correo,
                                        'Telefono': telefono,
                                        'paycon': newpaycon,
                                        'Modalidad': modalidad,
                                        'montoApagar': montoAcancelar,
                                        'fuenteOrigen': fuenteOrigen,
                                        'fechaPago': fechaPago,
                                        'referenciaPago': referenciaPago,
                                        'MontoPago': montoPago}
                elif first['paycon']=='PENDIENTE' : 
                        newpaycon = 'PENDIENTE'
                        updates = {'Nombres': nombres,
                                'Apellidos': apellidos,
                                'Email': correo,
                                'Telefono': telefono,
                                'paycon': newpaycon,
                                'fuenteOrigen': fuenteOrigen,
                                'fechaPago': fechaPago,
                                'referenciaPago': referenciaPago,
                                'montoPago': montoPago}
                #updates, cedula

                encprof.update(updates, cedula)
                try:
                    if pagoAdicional:
                            try: pagocomp.put(regPagoCom)
                            except: st.write('No hay registro de pagos complementarios')
                except:
                    st.write('****')
                registro = encprof.get(cedula)
                st.write('Sus datos han sido actualizados y a continuacion se muestra como quedaron guardados')
                col1, col2 = st.columns(2)
                with col1:
                        st.info('Cédula o documento de identificación : ')
                        st.write('**Nombres**')
                        st.success(registro['Nombres'], icon="📛")
                        st.write('**Correo electronico**')
                        st.info(registro['correo'], icon="✉️")
                        st.write('**Origen (Transferencia o Pago Movil)**')
                        st.success(registro['fuenteOrigen'], icon="💳")
                        st.write('**Nro de referencia del pago (últimos 4 dígitos)**')
                        st.info(registro['referenciaPago'], icon="🔢")
                with col2:
                        st.success(registro['key'], icon="🆔")
                        st.write('**Apellidos**')
                        st.info(registro['Apellidos'], icon="ℹ️")
                        st.write('**Teléfono**')
                        st.success(registro['Telefono'], icon="📞")
                        st.write('**Fecha de Pago**')
                        st.info(registro['fechaPago'], icon="📆")
                        st.write('**Monto de Pago**')
                        st.success(registro['montoPago'], icon="💴")
                try: 
                        st.success('Su pago adicional fue registrado exitosamente. Esperamos confirmarlo a la brevedad posible y de ese modo actualizar su status de pago')
                        pcomp = pagocomp.fetch() 
                        bregPagoComp = [x for x in pcomp.items if x['key']==cedula+'-'+referenciaPagoComp]
                        #st.write(bregPagoComp[0])
                        st.info('💳Modo de pago: :green[**' +bregPagoComp[0]['modoPago']+'**]'+'◀️➖➖➖▶️'+'Nro de referencia del pago : :orange[**' + bregPagoComp[0]['referencia']+'**]🔢')
                        st.success('💴Monto de Pago: :orange[ **' + str(bregPagoComp[0]['monto'])+'**]'+'◀️➖➖➖▶️'+'Fecha de Pago: :orange[**'+bregPagoComp[0]['fecha']+'**]📆')
                        #st.succes('Monto de Pago: :orange[**'+bregPagoComp[0]['monto']+'**]💴')
                        #st.succes('Monto de Pago: :orange[**'+bregPagoComp[0]['monto']+'**]💴'+'◀️➖➖➖▶️'+'Fecha de Pago: :green[**'+bregPagoComp[0]['fecha']+'**]📆')
                except:
                        st.write('No hay registro de  complementarios') 
                        

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
