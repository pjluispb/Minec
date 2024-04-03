import pandas as pd
from deta import Deta
import streamlit as st
from collections import OrderedDict

deta = Deta(st.secrets.deta_key)

pronda2023 = deta.Base('PRONDAMIN2023-Final')
pronda2022 = deta.Base('PRONDANMIN-2022')
pronda2024 = deta.Base('Prondamin2024B')
# pronda2021 = deta.Base('PRONDANMIN-2021')
# pronda2020 = deta.Base('PRONDANMIN-2020')

p23 = pronda2023.fetch(limit=5000)
p22 = pronda2022.fetch(limit=5000)
p24 = pronda2024.fetch(limit=5000)
# p21 = pronda2021.fetch(limit=5000)
# p20 = pronda2020.fetch(limit=5000)

dfp23 = pd.DataFrame(p23.items)
dfp22 = pd.DataFrame(p22.items)
dfp24 = pd.DataFrame(p24.items)
# dfp21 = pd.DataFrame(p21.items)
# dfp20 = pd.DataFrame(p20.items)

#dfp23ri = dfp23.reindex(columns=['CEDULA', 'NOMBRES', 'APELLIDOS',  'EMAIL', 'TELEFONO', 'DISTRITO', 'CATEGORIA', 'CURSOREALIZADO', 'MODALIDAD', 'STATUS', 'REPORTECERTIF', 'key'])

#dfp22ri = dfp22.reindex(columns=['CEDULA', 'NOMBRES', 'APELLIDOS',  'EMAIL', 'TELEFONO', 'DISTRITO', 'CATEGORIA', 'CURSOREALIZADO', 'MODALIDAD', 'STATUS', 'REPORTECERTIF', 'key'])

dfp23ri = dfp23.reindex(columns=['CEDULA', 'NOMBRES', 'APELLIDOS'])
dfp22ri = dfp22.reindex(columns=['CEDULA', 'NOMBRES', 'APELLIDOS'])

'Data 2023'
dfp23ri
'Data 2022'
dfp22ri


dftl23 = dfp23ri.values.tolist()
dftl22 = dfp22ri.values.tolist()

dftlcom1 = dftl23
dftlcom1.extend([elemento for elemento in dftl22 if elemento not in dftl23])

dftlcom1

dfcom1 = pd.DataFrame(dftlcom1, columns=['cedula', 'nombre', 'apellido'])

dfcom1
#-----------------------------------------------------------------
lista=[[123, 'Pedro', 'Perez', 'Saludos', ['+584247765285', '02742521632'], ['pepe@yuhu.com','peperez@yahu.com'], 
        ['Ministro Cristiano', 'Virtual', 'Aprobado', 'SI', 'Ministro Distrital', 'Centro',],
        ['Ministro Cristiano', 'Presencial', 'Aprobado', 'SI', 'Ministro Distrital', 'Centro',],123
        ], 
       [456, 'Maria', 'Perez', 'Hola', ['+584247765285'], ['mape@yuhu.com','mariperez@yahu.com'],
        ['Ministro Cristiano', 'Virtual', 'Aprobado', 'SI', 'Ministro Distrital', 'Centro',],
        ['Ministro Licenciado', 'Virtual', 'Aprobado', 'SI', 'Ministro Cristiano', 'Centro',],456
        ],
        ]
# lista
dflista = pd.DataFrame(lista, columns=['id','nombre','apellido','text', 'telefonos', 'emails', 'Periodo 2022', 'Periodo 2023', 'key'])
dflista
#--------------------------------------------------------------------

newl=[]
for t in range(3000):
    #dftlcom1[t]
    id = dftlcom1[t][0]
    c2023 = pronda2023.get(id)
    c2022 = pronda2022.get(id)

    emails=[c2023['EMAIL'] if c2023 != None else '-', c2022['EMAIL'] if c2022 != None else '-']
    try: emails.remove('-')
    except: pass
    try: emails.remove('-')
    except: pass
    semails = set(emails)
    emails = list(semails)
    
    telf=[str(c2023['TELEFONO']) if c2023 != None else '-', str(c2022['TELEFONO']) if c2022 != None else '-']
    try: telf.remove('-')
    except: pass
    try: telf.remove('-')
    except: pass
    #'telf = ', telf
    
    def normalizar_elemento(elemento):
        # Eliminar espacios en blanco al principio y al final
        elemento = elemento.strip()

        # Verificar si el elemento comienza con '0'
        if not elemento.startswith('0'):
            elemento = '0' + elemento

        # Verificar si el código después del '0' es válido
        codigos_validos = ['416', '426', '414', '424', '412']
        codigo = elemento[1:4]
        if codigo not in codigos_validos:
            # Si no es válido, usar '416' como código predeterminado
            elemento = '0' + '416' + elemento[4:]

        # Asegurar que la longitud total sea 12
        elemento = elemento[:12]

        return elemento   

    telefonos = []
    for ele in telf:
        ntelf = normalizar_elemento(ele)
        telefonos.append(ntelf)
    #telefonos
    stelf = set(telefonos)
    telefonos2 = list(stelf)
    #telefonos2

    nuevor ={'key':dftlcom1[t][0], 'nombre':dftlcom1[t][1], 'apellido':dftlcom1[t][2], 'distrito':c2023['DISTRITO'] if c2023 != None else c2022['DISTRITO'], 'categoría':c2023['CATEGORIA'] if c2023 != None else c2022['CATEGORIA'], 'emails':emails, 'teléfonos':telefonos2, 'curso':'-', 'modalidad':'-', 'montoApagar':'-', 'fechaPago':'-', 'fuenteOrigen':'-', 'montoPago':'-', 'paycon': 'NO', 'referenciaPago':'-'}

    pronda2024.put(nuevor)
    # nuevor
    newl.append(nuevor)
'==================================================================='
newl
#df = df.reindex(columns=['cedula', 'Nombres', 'Apellidos','Categoria','Email','Telefono','Distrito','Modalidad','Status', 'ReporteCertif','paycon','fuenteOrigen','referenciaPago','fechaPago','montoPago']) #Reordena las columnas como se mostraran
#df.style.apply(row_style, axis=1)  #Coloriza las filas

dfp24_ordenado = dfp24.reindex(columns=['key', 'nombre', 'apellido', 'distrito', 'categoría', 'teléfonos', 'emails'])
dfp24_ordenado






