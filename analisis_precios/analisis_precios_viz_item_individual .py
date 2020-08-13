# !pip install matplotlib
# !pip install seaborn
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

input_path=''
df_total=pd.read_csv(input_path)
data=df_total.copy()

# Price distribution box plot
x_label='Período'
y_label='Precio unitario en pesos corrientes'
sns.set(style="ticks", palette="pastel", rc={'figure.figsize':(8,8)})
ax = sns.boxplot(x='emergencia', y='precio_unitario_actualizado_mayo20', data=data, palette=["m", "g"])
ax = sns.stripplot(x='emergencia', y='precio_unitario_actualizado_mayo20', data=data, color="orange", jitter=0.2, size=7)
plt.xlabel(x_label, fontsize=15)
plt.ylabel(y_label, fontsize=15)
sns.despine(offset=10, trim=True)

# Price distribution & procurement method
sns.catplot(x='emergencia', y='precio_unitario_actualizado_mayo20', data=data, hue='tipo_procedimiento',
            palette="husl",
            kind="swarm",height=7, s=10)
plt.xlabel('Período', fontsize=15)
plt.ylabel('Precio unitario en pesos corrientes', fontsize=15)
sns.despine(offset=10, trim=True)

# Price distribution & type of contrac
sns.catplot(x='emergencia', y='precio_unitario_actualizado_mayo20', data=data,hue='contratacion',
            palette="husl",
            kind="swarm",height=7, s=10)
plt.xlabel('Período', fontsize=15)
plt.ylabel('Precio unitario en pesos corrientes', fontsize=15)
sns.despine(offset=10, trim=True)