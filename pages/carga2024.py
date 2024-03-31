
import pandas as pd
from deta import Deta
import streamlit as st

deta = Deta(st.secrets["deta_key"])
prondafull = deta.Base('ProndanminFull01')
prondafull2023 = prondafull.fetch()
pronda2024 = deta.Base('Prondamin2024A')
pronda2024f = pronda2024.fetch()

dfprondafull2023 = pd.DataFrame(prondafull2023.items)
dfpronda2024A = pd.DataFrame(pronda2024f.items)

dfprondafull2023
dfpronda2024A

df_out_dict = dfprondafull2023.to_dict('records')

cont = 0
for registro in df_out_dict:                             #loop que guarda e imprime los registros 
    # st.write(cont, registro)                            #de cada row o fila en la db en deta
    # registro['Apellidos'], registro['key']
    newregistro = registro
    newregistro['Modalidad']='-'
    newregistro['MontoApagar']='-'
    newregistro['ReporteCertif']='-'
    newregistro['Status']='-'
    newregistro['fechaPago']='-'
    newregistro['fuenteOrigen']='-'
    newregistro['paycon']='NO'
    newregistro['referenciaPago']='-'
    newregistro['CControlColor']='-'
    newregistro['Diferencia']='-'
    newregistro['Teléfono']='-'
    newregistro['correo']='-'
    newregistro['fecyhora']='-'
    newregistro['pagoComplementario']='-'
    newregistro['pagoF']=[]
    newregistro['pagosCompReg']='-'
    newregistro['pagosFraccionados']=[]
    newregistro['observacion']='-'
    #dnewreg = {cont:newregistro}
    #cont, 'dnewreg = ', dnewreg
    st.write(cont, newregistro)
    pronda2024.put(newregistro)
    cont+=1
    #if cont>5: break

print('---')
print(cont)
