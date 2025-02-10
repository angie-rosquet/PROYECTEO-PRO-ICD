import pandas as pd

# Supongamos que ya tienes tu DataFrame con los datos de los restaurantes
data = {
    "name": ["Restaurante A", "Restaurante B", "Restaurante C"],
    "address": ["Calle12 entre A y B, Centro Habana", "Calle 5 entre C y D, Playa", "Calle 10 entre E y F, Habana Vieja"],
}
restaurants_df = pd.DataFrame(data)

# Función para extraer el municipio
def extract_municipio(address):
    return address.split(",")[-1].strip()

# Aplicar la función para crear una nueva columna 'municipio'
restaurants_df['municipio'] = restaurants_df['address'].apply(extract_municipio)

# Filtrar por municipio
municipio_elegido = "Playa"  # Cambia esto por el municipio que desees
filtered_names = restaurants_df[restaurants_df['municipio'] == municipio_elegido]['name']

# Mostrar los nombres de los restaurantes filtrados
print(filtered_names)