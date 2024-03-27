import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from deta import Deta
from PIL import Image

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')

deta = Deta(st.secrets["deta_key"])
encprof = deta.Base('Prondamin2024A')
montopay = deta.Base('MontoAPagar')
montoApagar = montopay.fetch()

logina = st.session_state['logina']
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
                                nombres = ph1.text_input('Nombres :name_badge:', value = first['Nombres'])
                                apellidos = ph1.text_input('Apellidos:',value = first['Apellidos'])
                                correo = ph1.text_input('Correo Electrónico: 	:email:',value = first['Email'])
                                telefono = ph1.text_input('Teléfono: :telephone_receiver:',value = first['Telefono'])
                                distrito = ph1.text_input('Distrito:',value = first['Distrito'], disabled=True)
                                catasp = ph1.text_input('Categoría: :male-judge:',value = first['Categoria'], disabled=True)
                                ph1.write('---')
                                ph1.subheader('Datos acerca del pago')
                                if first['paycon']=='PENDIENTE':
                                        ph1.write('OBSERVACION: ⚠️:orange[****Su pago aún no ha sido confirmado****] ⚠️Puede realizar cambios en los datos de pago en el caso que sea necesario')
                                elif first['paycon']=='NO':
                                        ph1.write('OBSERVACION:👁️‍🗨️ :red[****Aún NO ha realizado ningún pago.****] 👁️‍🗨️Realize y registre su pago ahora')
                                else: ph1.write('OBSERVACION:✅ :green[****Pago confirmado. Inscripción realizada****] ✅Gracias por su diligencia')
                                modalidad = ph1.radio(label='Modalidad del curso', options=['Virtual', 'Presencial'], horizontal=True)
                                if modalidad=='Virtual': montoAcancelar = montoApagar.items[1]['MontoAPagarVirtual']
                                else: montoAcancelar = montoApagar.items[1]['MontoAPagarPresencial']
                                if first['paycon'] == 'SI': 
                                        valpay = True
                                        pagoConfirmado = 'SI'
                                else: 
                                        valpay = False
                                        pagoConfirmado = 'PENDIENTE'
                                        ph1.write('➡️➡️➡️ _Monto a cancelar por modalidad_   ↔️:red[ **'+ modalidad+ ': Bs '+montoAcancelar+'** ]')
                                fuenteOrigen = ph1.text_input('Origen del pago(Pago Móvil, Transferencia Bancaria)', value = first['fuenteOrigen'], disabled = valpay)
                                fechaPago = ph1.text_input('Fecha de pago', value = first['fechaPago'], disabled = valpay)
                                referenciaPago = ph1.text_input('Nro de referencia del pago (últimos 4 dígitos)', value = first['referenciaPago'], disabled = valpay)
                                montoPago = ph1.text_input('Monto pagado', value = first['montoPago'], disabled = valpay)
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
                updates = {'Nombres': nombres,
                           'Apellidos': apellidos,
                           'correo': correo,
                           'Teléfono': telefono,
                           'paycon': pagoConfirmado,
                           'fuenteOrigen': fuenteOrigen,
                           'fechaPago': fechaPago,
                           'referenciaPago': referenciaPago,
                           'montoPago': montoPago,
                           'MontoApagar': montoAcancelar,
                           'Modalidad': modalidad}

                encprof.update(updates, cedula)
                registro = encprof.get(cedula)
                col1, col2 = st.columns(2)
                with col1:
                        st.write('**Nombres**')
                        st.success(registro['Nombres'], icon="📛")
                        st.write('**Correo electronico**')
                        st.info(registro['correo'], icon="✉️")
                        st.write('**Modalidad**')
                        st.info(registro['Modalidad'], icon="🖥️")
                        st.write('**Origen de Pago**')
                        st.info(registro['fuenteOrigen'], icon="💳")
                        st.write('**Número de Referencia del Pago**')
                        st.info(registro['referenciaPago'], icon="🔢")
                with col2:
                        st.write('**Apellidos**')
                        st.info(registro['Apellidos'], icon="ℹ️")
                        st.write('**Teléfono**')
                        st.success(registro['Teléfono'], icon="📞")
                        st.write('**Monto A Cancelar**')
                        st.info(registro['MontoApagar'], icon="💴")
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
