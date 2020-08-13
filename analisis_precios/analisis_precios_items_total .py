# !pip install sklearn
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Defining series scaler
scaler = StandardScaler()
def escalador_serie(serie):
    return scaler.fit_transform(serie.values.reshape(-1, 1)).reshape(1, -1).tolist()[0]

# Loading csv
input_path='items_analisis_precios.csv'
items_analisis_precios=pd.read_csv(input_path)

# Scaled price series
serie_precios_estandarizada=[]
for i in items_analisis_precios['item'].unique():
    for j in escalador_serie(items_analisis_precios['precio_unitario_actualizado_mayo20'][items_analisis_precios['item']==i]):
        serie_precios_estandarizada.append(j)

items_analisis_precios['serie_precios_estandarizada']=pd.Series(serie_precios_estandarizada)

# Procurement method
items_analisis_precios['competencia']=pd.Series()
items_analisis_precios['competencia'][(items_analisis_precios['tipo_procedimiento']=='CME')|(items_analisis_precios['tipo_procedimiento']=='CDI')|(items_analisis_precios['tipo_procedimiento']=='CDE')]='No competitivo'
items_analisis_precios['competencia'][(items_analisis_precios['tipo_procedimiento']=='LPU')]='Competitivo'

# Saving csv
output_path=''
items_analisis_precios.to_csv('items_analisis_precios_escala.csv', index=False, sep=',', encodign='utf-8')