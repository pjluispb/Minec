
import pandas as pd
from deta import Deta
import streamlit as st

deta = Deta(st.secrets["deta_key"])

pronda2024 = deta.Base('Prondamin2024A')
pronda2024f = pronda2024.fetch()

dfpronda2024A = pd.DataFrame(pronda2024f.items)

dfpronda2024A

# dfpronda2024Atocsv = dfpronda2024A.to_csv('bkp_pronda2024A.csv', index=False)

#----------------------------------------------------------------------------------------
# --> loop para actualizar la bd con el campo paycon='NO' y los campos
# --> montoPago, MontoApagar, Modalidad, fuenteOrigen, fechaPago, referenciaPago = '-'
# cont=0
# for index, row in dfpronda2024A.iterrows():    
#     registro = {'paycon':'NO', 'montoPago':'-', 'MontoApagar':'-', 'Modalidad':'-', 'fuenteOrigen':'-', 'fechaPago':'-', 'referenciaPago':'-'}
#     st.write(cont,' ==> actualizando registro: ', registro, 'con clave: ', row['key'])
#     pronda2024.update(registro, str(row['key']))
#     cont+=1
#----------------------------------------------------------------------------------------

# --> loop para actualizar la bd 
# --> cambiando el valor de los  campos Categoria 
# --> de 'Ministro Distrital' a 'Ministro Cristiano'
# cont=0
# for index, row in dfpronda2024A.iterrows():
#     if row['Categoria']=='Ministro Distrital':
#         registro = {'Categoria': 'Ministro Cristiano' }
#         st.write(cont,' ==> actualizando registro: ', registro, 'con clave: ', row['key'])
#         pronda2024.update(registro, str(row['key']))
#         cont+=1
#------------------------------------------------------------------------------------------

