import pandas as pd
import streamlit as st
import datetime as datetime
from streamlit_extras.switch_page_button import switch_page
from deta import Deta
from PIL import Image



imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')

deta = Deta(st.secrets["deta_key"])
encprof = deta.Base('Prondamin2024B')
montopay = deta.Base('MontoAPagar')
montoApagar = montopay.fetch()

logina = st.session_state['logina']
#logina
#logina['tipou']
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
        with st.expander(label="Actualizar datos del ministro", expanded=True):
                ph1=st.container() 
                ph1.subheader(' Actualizar datos del ministro')
                # ch_data = False
                cedula = ph1.text_input('Número de cédula y/o documento de identidad :id:',key='iced',placeholder='ingrese su ID')
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
                                ph1.text('Edite los siguientes campos')
                                nombres = ph1.text_input('Nombres :name_badge:', value = first['nombre'])
                                apellidos = ph1.text_input('Apellidos:',value = first['apellido'])
                                correo = ph1.text_input('Correo Electrónico: 	:email:',value = first['emails'][0])
                                telefono = ph1.text_input('Teléfono: :telephone_receiver:',value = first['teléfonos'][0])
                                distrito = ph1.text_input('Distrito:',value = first['distrito'], disabled=True)
                                if logina['tipou']=='Registrador':
                                        catasp = ph1.text_input('Categoría: :male-judge:',value = first['categoría'], disabled=True)
                                if logina['tipou']=='Registrador Especial':
                                        vacat = first['categoría']
                                        catpos = ['Ministro Ordenado', 'Ministro Licenciado', 'Ministro Cristiano', 'Ministro Distrital', 'Ministro Otro', '-']
                                        ph1.write('El grado ministerial registrado actualmente en nuestra base de datos es de: :blue[ **'+vacat+'** ]')
                                        #ph1.write('Si desea cambiarlo/actualizarlo seleccione uno de los siguientes')
                                        catasp2 = ph1.selectbox('Si desea cambiarlo/actualizarlo seleccione uno de los siguientes. :orange[**OJO: debes estar muy seguro del cambio**] ', ['Ministro Ordenado', 'Ministro Licenciado', 'Ministro Cristiano', 'Ministro Distrital', '-'], index=None,  placeholder='Seleccione una opción')
                                        catasp = catasp2 if catasp2 != None else vacat
                                ph1.write('---')
                                ph1.subheader('Datos acerca del pago')
                                if first['paycon']=='PENDIENTE':
                                        ph1.write('OBSERVACIÓN: ⚠️:orange[****Su pago aún no ha sido confirmado****] ⚠️')
                                        ph1.write('Puede realizar cambios en los datos de pago en el caso que sea necesario')
                                        ph1.write('***')
                                elif first['paycon']=='NO':
                                        ph1.write('OBSERVACIÓN:👁️‍🗨️ :red[****Aún NO se ha registrado ningún pago.****] 👁️‍🗨️')
                                        ph1.write(' :blue[**RealiCe y registre su pago ahora**]')
                                        ph1.write('***')
                                else: 
                                        ph1.write('OBSERVACIÓN:✅ :green[****Pago confirmado. Inscripción realizada****] ✅Gracias por registrarte y por tu diligencia')
                                        ph1.write('Te invitamos a unirte al chat de PRONDAMIN 2024')
                                        ph1.link_button(label='Grupo de WhatsApp PRONDAMIN2024', url='https://chat.whatsapp.com/KmDnXJp1CF23mXe4cU3GEG')
                                modabase = ['Virtual', 'Presencial', '-']
                                #first['modalidad']
                                moda = first['modalidad']
                                modaindex = modabase.index(moda)
                                modalidad = ph1.radio(label='Modalidad del curso', options=['Virtual', 'Presencial'], horizontal=True, index=None if moda=='-' else modaindex)
                                if modalidad=='Virtual': 
                                        montoAcancelar = montoApagar.items[2]['MontoAPagarVirtual']
                                        modalidadmsg = 'Virtual'
                                elif modalidad=='Presencial': 
                                        montoAcancelar = montoApagar.items[2]['MontoAPagarPresencial']
                                        modalidadmsg = 'Presencial'
                                else: 
                                        montoAcancelar = '0'
                                        modalidadmsg = 'No Seleccionado'
                                if first['paycon'] == 'SI': 
                                        valpay = True
                                        pagoConfirmado = 'SI'
                                else: 
                                        valpay = False
                                        pagoConfirmado = 'PENDIENTE'
                                        ph1.write('➡️➡️ _Monto a cancelar por modalidad:_   :red[ **'+ str(modalidadmsg) + '** ]'+', Bs :blue[ **'+montoAcancelar+'** ]')
                                #fuenteOrigen = ph1.text_input('Origen del pago(Pago Móvil, Transferencia Bancaria)', value = first['fuenteOrigen'], disabled = valpay)
                                foribase = ['Pago Móvil', 'Transferencia Bancaria', '-']
                                fori = first['fuenteOrigen']
                                forindex = foribase.index(fori)
                                fuenteOrigen = ph1.radio('Fuente/Origen del pago', ['Pago Móvil', 'Transferencia Bancaria'], index=None if fori=='-' else forindex, horizontal=True, disabled=valpay)
                                #fechaPago = ph1.text_input('Fecha de pago', value = first['fechaPago'], disabled = valpay)
                                fpago = first['fechaPago']
                                if fpago != '-': fpago2 = datetime.datetime.strptime(fpago, "%d/%m/%Y")
                                #if fpago != '-': 
                                fechaPago2 = ph1.date_input('Fecha de pago', value=None if fpago == '-' else fpago2, format="DD/MM/YYYY")
                                fechaPago = fechaPago2.strftime("%d/%m/%Y") if fechaPago2 != None else '-'
                                referenciaPago = ph1.text_input('Nro de referencia del pago (últimos 4 dígitos)', value = first['referenciaPago'], disabled = valpay, max_chars=4)
                                #montoPago = ph1.text_input('Monto pagado', value = first['montoPago'], disabled = valpay)
                                montoPago2 = ph1.number_input('Monto pagado', value = None if first['montoPago']=='-' else float(first['montoPago']), placeholder='escribe un número')
                                montoPago = str(montoPago2) if montoPago2 != None else '-'
                        else:
                                st.warning('El número de documento de identidad:id: ingresado NO aparece en nuestra base de datos.:file_cabinet: :arrow_right: intente de nuevo')
if ch_data:
        confirmar = st.radio('¿Confirma la edición de la data y su registro en el próximo curso de MINEC?',('SI','NO'), index=1, horizontal=True)
        if confirmar=='SI':
                edo='confirmar'
                #st.info('Actualizando Datos:  '+edo)
                hide01()
                b1=True
        else:    
                st.warning('Por favor confirme la edición para proceder a la actualización:  ')

if b1:
        with st.expander("ESTOS SON LOS DATOS ACTUALIZADOS", expanded=True):
                b0=False
                if modalidad==None: modalidad='-'
                if fuenteOrigen==None: fuenteOrigen='-'
                if referenciaPago=='-': pagoConfirmado='NO'
                updates = {'nombre': nombres,
                           'apellido': apellidos,
                           'categoría': catasp,
                           'emails': [correo],
                           'teléfonos': [telefono],
                           'paycon': pagoConfirmado,
                           'fuenteOrigen': fuenteOrigen,
                           'fechaPago': fechaPago,
                           'referenciaPago': referenciaPago,
                           'montoPago': montoPago,
                           'montoApagar': str(montoAcancelar),
                           'modalidad': modalidad}

                encprof.update(updates, cedula)
                registro = encprof.get(cedula)
                col1, col2 = st.columns(2)
                with col1:
                        st.write('**Nombres**')
                        st.success(registro['nombre'], icon="📛")
                        st.write('**Correo electronico**')
                        st.info(registro['emails'][0], icon="✉️")
                        st.write('**Modalidad**')
                        st.info(registro['modalidad'], icon="🖥️")
                        st.write('**Origen de Pago**')
                        st.info(registro['fuenteOrigen'], icon="💳")
                        st.write('**Número de Referencia del Pago**')
                        st.info(registro['referenciaPago'], icon="🔢")
                        
                with col2:
                        st.write('**Apellidos**')
                        st.info(registro['apellido'], icon="ℹ️")
                        st.write('**Teléfono**')
                        st.success(registro['teléfonos'][0], icon="📞")
                        st.write('**Monto A Cancelar**')
                        st.info(registro['montoApagar'], icon="💴")
                        st.write('**Fecha de Pago**')
                        st.info(registro['fechaPago'], icon="📆")
                        st.write('**Monto Pagado**')
                        st.info(registro['montoPago'], icon="💴")

                # #df.to_csv("Prondanmin23.csv")
                # df.to_csv(urlcsv)
                
        recomenzar = st.button('Volver a Editar')
        if recomenzar:
                cedula = ''
                switch_page('reiniciar')
        
st.write('----------------')
regresar = st.button('Volver a Principal')
if regresar:
    switch_page('logmi')
st.page_link("pages/home2024.py", label="Inicio", icon="🏠")
