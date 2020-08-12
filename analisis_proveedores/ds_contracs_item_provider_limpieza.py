#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np

# Function: create new features in pd DF

def limpieza_ds_contracs_provider(ds):
    
    ds['contracts/0/period/startDate']=pd.to_datetime(ds['contracts/0/period/startDate'], format='%Y-%m-%d %H:%M:%S').copy()

    ds['anio_inicio_contrato']=ds['contracts/0/period/startDate'].apply(lambda x: str(x.year))

    ds['2019']=pd.Series()
    
    ds['2020']=pd.Series()

    ds['pre_emergencia']=pd.Series()
    
    ds['pos_emergencia']=pd.Series()

    ds['2019'][contracs_items_provider['anio_inicio_contrato'].isin(['2019.0'])]=1
    
    ds['2020'][contracs_items_provider['anio_inicio_contrato'].isin(['2020.0'])]=1
  
    ds['pre_emergencia'][ds['contracts/0/period/startDate']<'2020-03-11 00:00:00']=1

    ds['pos_emergencia'][ds['contracts/0/period/startDate']>='2020-03-11 00:00:00']=1
    
    return ds

# Local paths
input_path='contracs_items_provider.csv'

output_path=''

# Load CSV
contracs_items_provider=pd.read_csv(input_path)

# Use function
contracs_item_provider_limpio=limpieza_ds_contracs_provider(contracs_items_provider)

# Save csv
contracs_item_provider_limpio.to_csv(output_path, index=False, sep=',', encoding='utf-8')

