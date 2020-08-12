import pandas as pd
import requests
import urllib.parse


# Function: Select relevant items from before emergency DF

def item_pre_emergencia(lista_item):
    return contracs_items_pre_emergencia[
        contracs_items_pre_emergencia['contracts/0/items/0/classification/id'].isin(lista_item)].reset_index(drop=True)


# Function: new additional features and merge with IPC

def merge_ipc(df):
    df['anio_mes'] = pd.to_datetime(
        df['contracts/0/dateSigned']).apply(lambda x: x.year).astype(str) + '-' + pd.to_datetime(
        df['contracts/0/dateSigned']).apply(lambda x: x.month).astype(str)

    df = pd.merge(df, ipc, how='left', on='anio_mes')

    df['precio_unitario_actualizado_mayo20'] = df['contracts/0/items/0/unit/value/amount'] * (
                1 + df['variación_mayo_2020'])

    df['precio_unitario_actualizado_mayo20'] = df['precio_unitario_actualizado_mayo20'].fillna(
        df['contracts/0/items/0/unit/value/amount'])

    return df


# Function: Merge df with monthly avg TCN

def merge_tcn(df):
    df = pd.merge(df, tc_prom_peso_dolar, how='left', on='anio_mes')

    df['precio_unitario_dolares'] = df['contracts/0/items/0/unit/value/amount'] / df['Valor']

    return df


# Function: Select relevant columns from before emergency df

def columnas_interes(df):
    df = df[['tipo_procedimiento', 'contratacion', 'precio_unitario_actualizado_mayo20', 'precio_unitario_dolares']]

    df['emergencia'] = 'pre emergencia'

    return df


# Function: additional features

def procedimiento_contratacion(df):
    df['tipo_procedimiento'] = df['ocid'].str.extract('-([A-Z]+)\d+')[0]

    df['contratacion'] = df['contracts/0/id'].str.extract('([a-z]+)-')[0]

    return df


# Funciones emergencia
# Function: Select relevant items from emergency DF

def item_pos_emergencia(lista_item):
    return contracs_items_emergencia[
        contracs_items_emergencia['contracts/0/items/0/classification/id'].isin(lista_item)].reset_index(drop=True)


# Function: Select relevant columns from emergency df

def columnas_interes_emergencia(df):
    df = df[['tipo_procedimiento', 'contratacion', 'precio_unitario_actualizado_mayo20', 'precio_unitario_dolares']]

    df['emergencia'] = 'emergencia'

    return df


# Function: Merge IPC with CDE

def merge_ipc_28_8(df):
    df['anio_mes'] = pd.to_datetime(
        df['sancion']).apply(lambda x: x.year).astype(str) + '-' + pd.to_datetime(
        df['sancion']).apply(lambda x: x.month).astype(str)

    df = pd.merge(df, ipc, how='left', on='anio_mes')

    df['precio_unitario_actualizado_mayo20'] = df['precio_unitario'] * (1 + df['variación_mayo_2020'])

    return df


# Function: Merge TCN with CDE

def merge_tcn_28_8(df):
    df = pd.merge(df, tc_prom_peso_dolar, how='left', on='anio_mes')

    df['precio_unitario_dolares'] = df['precio_unitario'] / df['Valor']

    return df


# Select relevant columns

def columnas_interes_28_8(df):
    df = df[['precio_unitario_actualizado_mayo20', 'precio_unitario_dolares']]
    df['emergencia'] = 'emergencia'
    df['tipo_procedimiento'] = 'CDE'
    df['contratacion'] = 'occ'

    return df


# function: call API argentinian consumer's price index(cpi)

def get_api_call(ids, **kwargs):
    API_BASE_URL = "https://apis.datos.gob.ar/series/api/"
    kwargs["ids"] = ",".join(ids)
    return "{}{}?{}".format(API_BASE_URL, "series", urllib.parse.urlencode(kwargs))


# List of SKU code (catalog code) of item
item = ['']

# Create df with cpi
ipc = pd.read_csv(get_api_call(
    ["148.3_INIVELNAL_DICI_M_26"],
    format="csv", start_date=2018
))

# empty list
variacion_mayo_2020 = []

# get cpi variation
for i in ipc['ipc_nivel_general_nacional']:
    variacion_mayo_2020.append((ipc['ipc_nivel_general_nacional'].iloc[-1] / i) - 1)

# adding features to ipc df
ipc['variación_mayo_2020'] = pd.Series(variacion_mayo_2020)
ipc['anio'] = pd.to_datetime(ipc['indice_tiempo']).apply(lambda x: x.year)
ipc['mes'] = pd.to_datetime(ipc['indice_tiempo']).apply(lambda x: x.month)
ipc['anio_mes'] = ipc['anio'].astype(str) + '-' + ipc['mes'].astype(str)
ipc = ipc[['ipc_nivel_general_nacional', 'variación_mayo_2020', 'anio_mes']]

# loading csv
imput_path_contracs_items = ''
imput_path_contratacion_directa_emergencia = ''
imput_path_tcv_peso_dolar = ''

contracs_items = pd.read_csv(imput_path_contracs_items)
contratacion_directa_emergencia = pd.read_csv(imput_path_contratacion_directa_emergencia)
tcv_peso_dolar = pd.read_csv(imput_path_tcv_peso_dolar)

# Creating new feature
tcv_peso_dolar['anio_mes'] = pd.to_datetime(tcv_peso_dolar['Fecha']).apply(lambda x: x.year).astype(
    str) + '-' + pd.to_datetime(tcv_peso_dolar['Fecha']).apply(lambda x: x.month).astype(str)

# Creating avg TCN
tc_prom_peso_dolar = tcv_peso_dolar.groupby('anio_mes').mean().reset_index().sort_values('anio_mes')

# Selecting before emergency period
contracs_items_pre_emergencia = contracs_items[(contracs_items['contracts/0/dateSigned'] >= '2018-03-01') & (
            contracs_items['contracts/0/dateSigned'] < '2020-03-01')].reset_index(drop=True)

# Selecting emergency period
contracs_items_emergencia = contracs_items[(contracs_items['contracts/0/dateSigned'] >= '2020-03-01')].reset_index(
    drop=True)

# Filtering CDE ds with "nombre_item"
contratacion_directa_emergencia = contratacion_directa_emergencia[
    (contratacion_directa_emergencia['item'] == '')].reset_index(drop=True)

# Transforming before emergency ds (with indicated items (sku))
df_pre_emergencia = columnas_interes(procedimiento_contratacion(merge_tcn(merge_ipc(item_pre_emergencia(item)))))

# Transforming emergency ds
df_28_8_emergencia = columnas_interes_28_8(merge_tcn_28_8(merge_ipc_28_8(contratacion_directa_emergencia)))

df_BAC_emergencia = columnas_interes(procedimiento_contratacion(merge_tcn(merge_ipc(item_pos_emergencia(item)))))

df_emergencia = pd.concat([df_BAC_emergencia, df_28_8_emergencia]).reset_index(drop=True)

# Add feature
df_emergencia['emergencia'] = 'emergencia'

# Concat before emergency and emergency DF
df_total = pd.concat([df_emergencia, df_pre_emergencia]).reset_index(drop=True)

# Save csv
output_path = ''

df_total.to_csv(output_path, index=False, sep=',', encoding='utf-8')