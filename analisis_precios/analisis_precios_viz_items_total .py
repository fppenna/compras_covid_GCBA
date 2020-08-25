import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

input_path=''
items_analisis_precios_escala=pd.read_csv(input_path)

# Gráfico con distribución de precios en escala, procurement method  y período
sns.catplot(x='competencia', y='serie_precios_estandarizada', data=items_analisis_precios_escala,hue='emergencia',
            palette="husl", height=7, s=5,kind="swarm")
plt.axhline(0, color='green')
plt.xlabel('Tipo de procedimiento', fontsize=15)
plt.ylabel('Precio unitario en pesos corrientes estandarizado', fontsize=15)
sns.despine(offset=10, trim=True)

# Gráfico con ditribución de precios en escala, procurement method y período
sns.catplot(x='tipo_procedimiento', y='serie_precios_estandarizada', data=items_analisis_precios_escala,hue='emergencia',
            palette="husl", height=7, s=5,kind="swarm")
plt.axhline(0, color='green')
plt.xlabel('Tipo de procedimiento', fontsize=15)
plt.ylabel('Precio unitario en pesos corrientes estandarizado', fontsize=15)
sns.despine(offset=10, trim=True)

# Gráfico con distribución de precios en escala, tipo de contrato y período
sns.catplot(x='contratacion', y='serie_precios_estandarizada', data=items_analisis_precios_escala,hue='emergencia',
            palette="husl", height=7, s=5,kind="swarm")
plt.axhline(0, color='green')
plt.xlabel('Modalidad de contratación', fontsize=15)
plt.ylabel('Precio unitario en pesos corrientes estandarizado', fontsize=15)
sns.despine(offset=10, trim=True)

# Gráfico de densidad
sns.set(style="ticks", palette="pastel",rc={'figure.figsize':(10,10)})
p1=sns.kdeplot(items_analisis_precios_escala['serie_precios_estandarizada'][items_analisis_precios_escala['emergencia']=='pre emergencia'], shade=True, color="r")
p1=sns.kdeplot(items_analisis_precios_escala['serie_precios_estandarizada'][items_analisis_precios_escala['emergencia']=='emergencia'], shade=True, color="b")
plt.axvline(0, color='green')
plt.xlabel('Precio unitario en pesos corrientes estandarizado', fontsize=15)
plt.ylabel('Frecuencia', fontsize=15)
plt.legend(["Precios pre emergecia", "Precios emergencia"])
sns.despine(offset=10, trim=True)
