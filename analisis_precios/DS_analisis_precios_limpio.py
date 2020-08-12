import pandas as pd
pd.options.display.float_format = '{:.2f}'.format



# function: date parse
def formato_fechas(serie):
    return pd.to_datetime(serie, format='%Y-%m-%dT%H:%M:%S-03:00')


# function: set prices in ARS
def precios_pesos_cde(ds):
    ds['tipo_cambio'] = ds['tipo_cambio'].str.replace(',', '.').astype(float)

    ds['precio_unitario'][ds['moneda'] == 'USD'] = ds['precio_unitario'][ds['moneda'] == 'USD'] * \
                                                   ds['tipo_cambio'][ds['moneda'] == 'USD']

    return ds


# relevant columns list
lista_columnas_interes = ['ocid', 'id', 'contracts/0/id', 'contracts/0/awardID',
                          'contracts/0/title', 'contracts/0/description', 'contracts/0/status',
                          'contracts/0/period/startDate', 'contracts/0/period/endDate',
                          'contracts/0/period/durationInDays',
                          'contracts/0/value/amount', 'contracts/0/value/currency',
                          'contracts/0/dateSigned', 'contracts/0/items/0/id',
                          'contracts/0/items/0/description',
                          'contracts/0/items/0/classification/scheme',
                          'contracts/0/items/0/classification/id',
                          'contracts/0/items/0/quantity', 'contracts/0/items/0/unit/scheme',
                          'contracts/0/items/0/unit/name',
                          'contracts/0/items/0/unit/value/amount',
                          'contracts/0/items/0/unit/value/currency',
                          'tender/tenderPeriod/endDate']

# load csv files
path_gcba_contracs_items_jul = ''
path_contratacion_directa_emergencia_mar_jul = ''

contracs_items = pd.read_csv(path_gcba_contracs_items_jul)
contratacion_directa_emergencia = pd.read_csv(path_contratacion_directa_emergencia_mar_jul)

# Ds filter
contracs_items['contracts/0/dateSigned'] = formato_fechas(contracs_items['contracts/0/dateSigned'])
contracs_items['contracts/0/period/startDate'] = formato_fechas(contracs_items['contracts/0/period/startDate'])
contracs_items['contracts/0/period/endDate'] = formato_fechas(contracs_items['contracts/0/period/endDate'])
contracs_items = contracs_items[lista_columnas_interes]

# DS filter
contratacion_directa_emergencia = contratacion_directa_emergencia[
    (contratacion_directa_emergencia['estado_contratacion'] != 'rescindido') &
    (contratacion_directa_emergencia['estado_contratacion'] != 'Rescindida') &
    (contratacion_directa_emergencia['estado_contratacion'] != 'Recindida parcialmente') &
    (contratacion_directa_emergencia['estado_contratacion'] != 'no vigente')].reset_index(drop=True)

contratacion_directa_emergencia = precios_pesos_cde(contratacion_directa_emergencia)

# save csv files
output_path_contratacion_directa_emergencia = ''
output_path_contracs_items = ''

contracs_items.to_csv(output_path_contracs_items, index=False, sep=',', encoding='utf-8')
contratacion_directa_emergencia.to_csv(contratacion_directa_emergencia, index=False, sep=',', encoding='utf-8')