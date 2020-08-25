#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import datetime
from time import sleep
import os

## Scraping library
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


# Func. para corregir caracteres incorrectos

def limpieza_ds_bo(ds):
    ds['sancion'] = pd.to_datetime(ds['sancion'].str.replace('Sanción:\n', ''), format='%d/%m/%Y', errors='coerce')

    ds['fecha_publicacion'] = pd.to_datetime(ds['fecha_publicacion'].str.replace('Publicación:\n', ''),
                                             format='%d/%m/%Y', errors='coerce')

    ds = ds.sort_values(['sancion', 'fecha_publicacion']).reset_index(drop=True)

    ds['sintesis'] = ds['sintesis'].str.replace('Síntesis:\n', '')

    ds['organismo'] = ds['organismo'].str.replace('Organismo:\n', '')

    ds['sintesis'] = ds['sintesis'].str.replace('Ã³', 'Ó').str.replace('NÂ°', 'Nº').str.replace('Ãº', 'Ú').str.replace(
        'Ã\xad', 'Í').str.replace('Ã¡', 'Á')

    return ds


# Crear lista de URL del Boletin Oficial

url_BO = 'https://boletinoficial.buenosaires.gob.ar/normativaba/norma/'

start_id = '''dtype: int'''

stop_id = '''dtype: int'''

id_BO = [str(i) for i in range(start_id, stop_id, 1)]

list_url_BO = []

# For loop to create relevant BO URL

for i in id_BO:
    list_url_BO.append(url_BO + i)


# Chromedriver settings

option = webdriver.ChromeOptions()

option.add_argument('incognito')

# Local chrome driver path

chrome_driver_path = ''

# Browser settings

browser = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=option)

# Listas vacías para completar con  scraping
URL = []
titulo = []
sintesis = []
sancion = []
fecha_publicacion = []
organismo = []
texto = []

# Row number
row_num = 0

for i in list_url_BO:
    try:
        browser.get(i)
        URL.append(i)
        print(i)
        row_num = row_num + 1
        print(row_num)
        sleep(2)

        try:
            titulo.append(browser.find_elements_by_xpath('//*[@id="detalle_normativa"]/div[1]')[0].text)
            sleep(0.1)

        except:
            titulo.append('sin titulo')

        try:
            sintesis.append(browser.find_elements_by_xpath('//*[@id="detalle_normativa"]/div[2]')[0].text)
            sleep(0.1)

        except:
            sintesis.append('sin sintesis')

        try:
            fecha_publicacion.append(browser.find_element_by_xpath('//*[@id="detalle_normativa"]/div[3]').text)
            sleep(0.1)

        except:
            fecha_publicacion.append('sin fecha')

        try:
            sancion.append(browser.find_element_by_xpath('//*[@id="detalle_normativa"]/div[4]').text)
            sleep(0.1)

        except:
            sancion.append('sin fecha')

        try:
            organismo.append(browser.find_element_by_xpath('//*[@id="detalle_normativa"]/div[5]').text)
            sleep(0.1)

        except:
            organismo.append('sin organismo')

        try:
            browser.find_element_by_link_text('Texto original').click()
            sleep(1)
            texto.append(browser.find_element_by_xpath('//*[@id="collapseFive"]/div').text)
            print(browser.find_element_by_xpath('//*[@id="collapseFive"]/div').text)

        except:
            texto.append('sin texto')
    except:
        URL.append(i)
        titulo.append('no funciona -> ' + i)
        sintesis.append('no funciona -> ' + i)
        sancion.append('no funciona -> ' + i)
        fecha_publicacion.append('no funciona -> ' + i)
        organismo.append('no funciona -> ' + i)
        texto.append('no funciona -> ' + i)

# Creación del DataFrame usando listas completas

boletin_oficial = pd.DataFrame()
boletin_oficial['URL'] = pd.Series(URL)
boletin_oficial['titulo'] = pd.Series(titulo)
boletin_oficial['sintesis'] = pd.Series(sintesis)
boletin_oficial['sancion'] = pd.Series(sancion)
boletin_oficial['fecha_publicacion'] = pd.Series(fecha_publicacion)
boletin_oficial['organismo'] = pd.Series(organismo)
boletin_oficial['texto'] = pd.Series(texto)

# Corregir caracteres incorrectos
ds_boletin_oficial = limpieza_ds_bo(boletin_oficial)

# Serializar datos
csv_path = ''
ds_boletin_oficial.to_csv(csv_path, index=False, sep=',', encoding='utf-8')
