import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from deta import Deta
from PIL import Image

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')

deta = Deta(st.secrets["deta_key"])

logina = st.session_state['logina']
accesos = deta.Base('minec-accesos')
res=accesos.fetch()
#res.items
#st.write(len(res.items))
permisados=[]
for t in range(len(res.items)):
    if res.items[t]['tipou']=='Registrador Especial':
        permisados.append((res.items[t]['user'], res.items[t]['clave']))

#permisados
#logina
if (logina['user'], logina['clave']) not in permisados:
    st.write('No esta en permisados')
    switch_page('reiniciar03')


encprof = deta.Base('Prondamin2024A')
montopay = deta.Base('MontoAPagar')
montoApagar = montopay.fetch()
#st.write(montoApagar.items[0]['MontoAPagarVirtual'], montoApagar.items[0]['MontoAPagarPresencial'])

logina = st.session_state['logina']
#logina
st.image(imagen1)
st.image(imagen2)
st.title('Nuevo Registro')
#st.write('En Distrito : ****' + logina['Distrito'] + '****')
ph1 = st.container()
with st.form('nuevo registro'):
    cedula = st.text_input('Cédula de identidad y/o documento de identidad :id:')
    nombres = st.text_input('Nombres: :name_badge:')
    apellidos = st.text_input('Apellidos:')
    correo = st.text_input('Correo Electrónico: 	:email:')
    telefono = st.text_input('Teléfono: :telephone_receiver:')
    if logina['tipou']=='Registrador':
        distrito = logina['Distrito']
        st.write('Distrito : ****' + distrito + '****')
    else:
        distrito = st.selectbox('Distrito:',['Andino','Centro','Centro Llanos', 'Falcón','Lara', 'Llanos','Llanos Occidentales','Metropolitano','Nor Oriente','Sur Oriente','Yaracuy','Zulia'])
    categoria = st.selectbox(label= 'Categoría :', options=['Ministro Cristiano','Ministro Licenciado','Ministro Ordenado'])
    # modalidad = st.radio(label='Modalidad del curso', options=['Virtual', 'Presencial'], horizontal=True)
    # if modalidad=='Virtual': montoAcancelar = montoApagar.items[0]['MontoAPagarVirtual']
    # else: montoAcancelar = montoApagar.items[0]['MontoAPagarPresencial']
    # st.write('➡️➡️➡️ _Monto a cancelar por modalidad_   ↔️:red[ **'+ modalidad+ ': Bs '+montoAcancelar+'** ]')
    # pagoConfirmado = 'NO'
    # fuenteOrigen = st.text_input('Origen del pago(Transferencia o Pago Movil)', value = '-')
    # fechaPago = st.text_input('Fecha de pago _(dd/mm/aa)_', value='-')
    # referenciaPago = st.text_input('Nro de referencia del pago (últimos 4 dígitos)',value='-')
    # montoPago = st.text_input('Monto pagado', value='-')

    registrar = st.form_submit_button('Registrar la nueva entrada')
    if registrar:
        modalidad, montoAcancelar, pagoConfirmado, fuenteOrigen = '-', '-', '-', '-'
        fechaPago, referenciaPago, montoPago = '-', '-', '-'
        status, observacion =  'S/A', 'S/A'
        if (fuenteOrigen != '-') or (referenciaPago != '-') or (montoPago != '-') or (fechaPago != '-'):
            pagoConfirmado = 'PENDIENTE'
        else: 
            pagoConfirmado = 'NO'
        entradas = ['55',correo,apellidos,nombres,cedula,telefono,distrito,categoria,modalidad,status,observacion, fuenteOrigen, fechaPago, referenciaPago, montoPago]
        if '' in entradas:
            ph1.warning('Debe llenar todos los campos')
        else:                 # Agrega registro a la BD
            st.success('Se ha registrado una nueva entrada', icon="✅" )
            registro = {
                "key": cedula,
                "Email": correo,
                "Apellidos": apellidos,
                "Nombres": nombres,
                "Telefono": telefono,
                "Distrito": distrito,
                "Categoria": categoria,
                "Modalidad": modalidad,
                "Status": status,
                "ReporteCertif": observacion,
                'paycon': pagoConfirmado,
                'fuenteOrigen': fuenteOrigen,
                'fechaPago': fechaPago,
                'referenciaPago': referenciaPago,
                'montoPago': montoPago,
                'MontoApagar': montoAcancelar
                }
            #registro
            encprof.put(registro)
            st.write('** **')
            st.subheader('🗂️Ficha del Nuevo Registro')
            #st.subheader('Datos Personales')
            col1, col2 = st.columns(2)

            with col1:
                st.write('**Cédula**')
                st.success(registro['key'], icon="🆔")
                st.write('**Nombres**')
                st.info(registro['Nombres'], icon="📛")
                st.write('**Categoria**')
                st.info(registro['Categoria'], icon="💠")
                st.write('**Modalidad**')
                st.success(registro['Modalidad'], icon="💻")
                st.write('**Correo Electronico**')
                st.success(registro['Email'], icon="📧")
                st.write('--------------')
                # st.write('**Origen del Pago**')
                # st.success(registro['fuenteOrigen'], icon="📧")
                # st.write('**Número de Referencia del Pago**')
                # st.success(registro['referenciaPago'], icon="📧")
            with col2:
                st.write('**Teléfono**')
                st.info(registro['Telefono'], icon="📞")
                st.write('**Apellidos**')
                st.success(registro['Apellidos'], icon="ℹ️")
                st.write('**Distrito**')
                st.success(registro['Distrito'], icon="🗺️")
                st.write('**Status**')
                st.info(registro['Status'], icon="📝")
                st.write('**.**')
                st.success('-',icon="📧")
                st.write('-----------------')
                # st.write('**Fecha del Pago**')
                # st.success(registro['fechaPago'], icon="📧")
                # st.write('**Monto Pagado**')
                # st.success(registro['montoPago'], icon="📧")

regresar = st.button('Volver')
if regresar:
    switch_page('logmi')
st.page_link("pages/home2024.py", label="Inicio", icon="🏠")
