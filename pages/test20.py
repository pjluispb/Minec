import pandas as pd
from deta import Deta
import streamlit as st

deta = Deta(st.secrets.deta_key)

pronda2024 = deta.Base('Prondamin2024B')
p24 = pronda2024.fetch(limit=3000)
dfp24 = pd.DataFrame(p24.items)

dfp24