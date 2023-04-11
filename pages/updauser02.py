
import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from deta import Deta
from PIL import Image

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')

deta = Deta(st.secrets["deta_key"])
encprof = deta.Base('ProndanminFull01')
montopay = deta.Base('MontoAPagar')
montoApagar = montopay.fetch()

st.image(imagen1)
st.image(imagen2)

encprof = deta.Base('ProndanminFull01')
st.subheader('Módulo02 de actualización e inscripción en Prondanmin')
st.write('Solo para aquellos ministros cuya cédulas no aparecen en nuestra base de datos')
dbcontent = encprof.fetch(limit=5000).items
df = pd.DataFrame(dbcontent)
dttox = ['Sur', 'Andi', 'Metro', 'Yara']
seldttox = st.selectbox('Selecciona el Distrito al que perteneces',options=['Sur Oriente', 'Yaracuy', 'Zulia'])
dttosel = seldttox[:3]
#dttosel
dfdsel = df.loc[(df['key'].str.startswith(dttosel))]
dfdsel = dfdsel.reindex(columns=['Nombres','Apellidos','key','Categoria'])
#dfdsel = dfdsel.sort_values(by='Nombres')
dfdsel2 = dfdsel.loc[(dfdsel['Nombres']!=' ')]
#dfdsel2 = dfdsel.loc[str(dfdsel['Nombres'])=='Nan']
#dfdsel2
lnom=dfdsel2[['Nombres','Apellidos','Categoria','key']].values.tolist()
#lnom
lnomap=[str(n)+' '+str(a) for (n,a,c,k) in lnom if str(n)+' '+str(a)!='nan nan']
#lnomap
nombreyape = st.selectbox('Seleccione su nombre y apellido', lnomap)
regsel = [(nom,ap,cat,key) for (nom,ap,cat,key) in lnom if str(nom)+' '+str(ap) == nombreyape]
#regsel
ph1 = st.expander(label='Edita los siguientes datos del ministro')
datper = st.form('Datos Personales')
cedula = datper.text_input('Cédula y/o documento de identidad :id:', value = regsel[0][3])
nombres = datper.text_input('Nombres :name_badge:', value = regsel[0][0])
apellidos = datper.text_input('Apellidos:',value = regsel[0][1])
correo = datper.text_input('Correo Electrónico: 	:email:',value='-')
telefono = datper.text_input('Teléfono: :telephone_receiver:',value='-')
distrito = datper.text_input('Distrito:',value = seldttox, disabled=True)
catasp = datper.text_input('Categoría: :male-judge:',value = regsel[0][2], disabled=True)
confirmar = datper.form_submit_button('Actualizar Datos Personales')


# confirmar = st.radio('¿Confirma la edición de la data y su registro en el próximo curso de MINEC?',('SI','NO'), index=1, horizontal=True)
if confirmar:
        edo='confirmar'
        b1 = True
else:    
        #st.warning('Por favor confirme la edicion para proceder a la actualizacion:  ')
        b1 = False
if b1:
    with st.expander("ESTOS SON LOS DATOS ACTUALIZADOS", expanded=True):  
        newpaycon = 'NO'
        fuenteOrigen, referenciaPago = '-', '-'
        montoPago, fechaPago = '-', '-'
        newregistro = {'key': cedula,
                    'Nombres': nombres,
                    'Apellidos': apellidos,
                    'correo': correo,
                    'Teléfono': telefono,
                    'Distrito': distrito,
                    'Categoria': catasp,
                    'paycon': newpaycon,
                    'fuenteOrigen': fuenteOrigen,
                    'fechaPago': fechaPago,
                    'referenciaPago': referenciaPago,
                    'montoPago': montoPago,
                    'MontoApagar': '-',
                    'Modalidad': '-'}
        #updates, cedula
        cedulanew = cedula
        cedulaold = regsel[0][3]
        cedulanew, cedulaold
        #encprof.update(updates, cedula)
        encprof.put(newregistro)
        registro = encprof.get(cedulanew)
        #  ------ >>>   encprof.update({'Nombres':'Para borrar','Distrito':distrito,'paycon':'-'}, cedulaold)
        encprof.delete(cedulaold)
        #  ------ >>>   registroAnterior = encprof.get(cedulaold)
        #regdel

        st.write('Sus datos han sido actualizados y a continuacion se muestra como quedaron guardados')
        col1, col2 = st.columns(2)
        with col1:
                st.info('Cédula o documento de identificación : ')
                st.write('**Nombres**')
                st.success(registro['Nombres'], icon="📛")
                st.write('**Correo electronico**')
                st.info(registro['correo'], icon="✉️")
                st.write('**Distrito**')
                st.info(registro['Distrito'])
                # st.write('**Modalidad**')
                # st.info(registro['Modalidad'], icon="🖥️")
                # st.write('**Origen (Transferencia, Pago Movil)**')
                # st.info(registro['fuenteOrigen'], icon="💳")
                # st.write('**Nro de referencia del pago (últimos 4 dígitos)**')
                # st.info(registro['referenciaPago'], icon="🔢")
        with col2:
                st.info(registro['key'], icon="ℹ️")
                st.write('**Apellidos**')
                st.info(registro['Apellidos'], icon="ℹ️")
                st.write('**Teléfono**')
                st.success(registro['Teléfono'], icon="📞")
                st.write('**Categoría**')
                st.success(registro['Categoria'])
                # st.write('**Monto A Cancelar**')
                # st.info(registro['MontoApagar'], icon="💴")
                # st.write('**Fecha de Pago**')
                # st.info(registro['fechaPago'], icon="📆")
                # st.write('**Monto de Pago**')
                # st.info(registro['montoPago'], icon="💴")
        #--registroAnterior

        recomenzar = st.button('Re-iniciar')
        if recomenzar:
            cedula = ''
            switch_page('reinicia02')
#edo = 'inicial'
# def hide01():
#         b0=False
#         b1=True
#         return
# if edo=='inicial':
#         b0=True
#         b1=False
# elif edo=='confirmar':
#         b0=False
#         b1=True
# ch_data = False
# if b0:
#         with st.expander(label="-", expanded=True):
#                 ph1=st.container() 
#                 ph1.subheader(' Bienvenido ministro a la aplicación de registro en cursos de la MINEC')
#                 # ch_data = False
#                 cedula = ph1.text_input('Introduzca su número de cédula y/o documento de identidad :id: para comenzar',key='iced',placeholder='ingrese su ID')
#                 try:
#                         first = encprof.get(cedula)
#                 except:
#                         if cedula=='':
#                                 st.write('Ingrese un numero de cedula')
#                         else:
#                                 st.write('cedula no existe')
#                                 st.warning('''El número de cedula/id:id: NO aparece en nuestra base de datos.:file_cabinet:
#                                         :arrow_right: Tendrá que registrarse nuevamente y al momento de hacerlo deberá introducir un requerimiento de revisión de data.
#                                         Entonces procederemos a procesar su requerimiento y en un plazo:date: razonable le
#                                         daremos una respuesta adecuada. Gracias por su paciencia, pero le recordamos
#                                         que fue usted mismo quien inscribió sus datos en nuestra base de datos	:card_index:''')
#                                 newRegB = st.button('Ir a nuevo registro :new:')
#                                 if newRegB:
#                                         switch_page("newReg")
#                 else:
#                         #ph1.write(first)
#                         if first!=None:
#                                 cedmin = cedula
#                                 ch_data = True
#                                 ph1.text('Edite los siguientes campos')
#                                 nombres = ph1.text_input('Nombres :name_badge:', value = first['Nombres'])
#                                 apellidos = ph1.text_input('Apellidos:',value = first['Apellidos'])
#                                 correo = ph1.text_input('Correo Electrónico: 	:email:',value = first['Email'])
#                                 telefono = ph1.text_input('Teléfono: :telephone_receiver:',value = first['Telefono'])
#                                 distrito = ph1.text_input('Distrito:',value = first['Distrito'], disabled=True)
#                                 catasp = ph1.text_input('Categoría: :male-judge:',value = first['Categoria'], disabled=True)
#                                 ph1.write('---')
#                                 ph1.write('Datos acerca del pago')
#                                 modalidad = ph1.radio(label='Modalidad del curso', options=['Virtual', 'Presencial'], horizontal=True)
#                                 if modalidad=='Virtual': montoAcancelar = montoApagar.items[0]['MontoAPagarVirtual']
#                                 else: montoAcancelar = montoApagar.items[0]['MontoAPagarPresencial']
#                                 if first['paycon'] == 'SI': valpay = True
#                                 else: 
#                                         valpay = False
#                                         ph1.write('➡️➡️➡️ _Monto a cancelar por modalidad_   ↔️:red[ **'+ modalidad+ ': Bs '+montoAcancelar+'** ]')
#                                 pagoConfirmado = ph1.text_input('Pago Confirmado', value = first['paycon'], disabled = True)
#                                 fuenteOrigen = ph1.text_input('Origen del pago(Transferencia, Pago Movil)', value = first['fuenteOrigen'], disabled = valpay)
#                                 fechaPago = ph1.text_input('Fecha de pago _(dd/mm/aa)_', value = first['fechaPago'], disabled = valpay)
#                                 referenciaPago = ph1.text_input('Nro de referencia del pago (últimos 4 dígitos)', value = first['referenciaPago'], disabled = valpay)
#                                 montoPago = ph1.text_input('Monto pagado', value = first['montoPago'], disabled = valpay)
#                         else:
#                                 st.warning('El número de documento de identidad:id: ingresado **NO** aparece en nuestra base de datos.:file_cabinet: :arrow_right: intente de nuevo, y si luego de varios intentos no aparece su información, entonces tendrá que ponerse de acuerdo con el representante de MINEC de su distrito')
# if ch_data:
#         confirmar = st.radio('¿Confirma la edición de la data y su registro en el próximo curso de MINEC?',('SI','NO'), index=1, horizontal=True)
#         if confirmar=='SI':
#                 edo='confirmar'
#                 #st.info('Actualizando Datos:  '+edo)
#                 hide01()
#                 b1=True
#         else:    
#                 st.warning('Por favor confirme la edicion para proceder a la actualizacion:  ')

# if b1:
#         with st.expander("ESTOS SON LOS DATOS ACTUALIZADOS", expanded=True):
                
#                 b0=False
#                 if first['paycon']=='SI':  newpaycon = 'SI'
#                 elif first['paycon']=='NO': 
#                         if (fuenteOrigen != '-') or (referenciaPago != '-') or (montoPago != '-') or (fechaPago != '-'): 
#                                 newpaycon = 'PENDIENTE'
#                         else:   
#                                 newpaycon = 'NO'
#                                 fuenteOrigen, referenciaPago = '-', '-'
#                                 montoPago, fechaPago = '-', '-'
#                 else : newpaycon = 'PENDIENTE'

#                 updates = {'Nombres': nombres,
#                            'Apellidos': apellidos,
#                            'correo': correo,
#                            'Teléfono': telefono,
#                            'paycon': newpaycon,
#                            'fuenteOrigen': fuenteOrigen,
#                            'fechaPago': fechaPago,
#                            'referenciaPago': referenciaPago,
#                            'montoPago': montoPago,
#                            'MontoApagar': montoAcancelar,
#                            'Modalidad': modalidad}
#                 #updates, cedula

#                 encprof.update(updates, cedula)
#                 registro = encprof.get(cedula)
#                 st.write('Sus datos han sido actualizados y a continuacion se muestra como quedaron guardados')
#                 col1, col2 = st.columns(2)
#                 with col1:
#                         st.info('Cédula o documento de identificación : ')
#                         st.write('**Nombres**')
#                         st.success(registro['Nombres'], icon="📛")
#                         st.write('**Correo electronico**')
#                         st.info(registro['correo'], icon="✉️")
#                         st.write('**Modalidad**')
#                         st.info(registro['Modalidad'], icon="🖥️")
#                         st.write('**Origen (Transferencia, Pago Movil)**')
#                         st.info(registro['fuenteOrigen'], icon="💳")
#                         st.write('**Nro de referencia del pago (últimos 4 dígitos)**')
#                         st.info(registro['referenciaPago'], icon="🔢")
#                 with col2:
#                         st.info(registro['key'], icon="ℹ️")
#                         st.write('**Apellidos**')
#                         st.info(registro['Apellidos'], icon="ℹ️")
#                         st.write('**Teléfono**')
#                         st.success(registro['Teléfono'], icon="📞")
#                         st.write('**Monto A Cancelar**')
#                         st.info(registro['MontoApagar'], icon="💴")
#                         st.write('**Fecha de Pago**')
#                         st.info(registro['fechaPago'], icon="📆")
#                         st.write('**Monto de Pago**')
#                         st.info(registro['montoPago'], icon="💴")
                        

#                 # #df.to_csv("Prondanmin23.csv")
#                 # df.to_csv(urlcsv)
                
#         recomenzar = st.button('Re-iniciar')
#         if recomenzar:
#                 cedula = ''
#                 switch_page('reinicia02')
        
st.write('----------------')
# regresar = st.button('Volver a Principal')
# if regresar:
#     switch_page('logmi')
