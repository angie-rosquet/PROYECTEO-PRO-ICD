import pandas as pd
import json
import os
import glob

ruta = 'Lugares/'

restaurantes_datos = []

municipios = os.listdir(ruta)
for municipio in municipios :
    ruta_municipio = os.path.join(ruta, municipio)
if os.path.isdir(ruta_municipio):
    archivos_json = glob.glob(os.path.join(ruta_municipio, '*.json'))
    for archivo in archivos_json:
        with open(archivo, 'r', encoding='utf-8') as f:
            datos_json = json.load(f)
            datos_json['municipio'] = municipio
            restaurantes_datos.append(datos_json)


df_restaurantes = pd.DataFrame(restaurantes_datos)
pd.set_option('display.max_rows', None)
print(df_restaurantes)