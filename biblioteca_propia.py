import pandas as pd
import json
import os
import matplotlib.pyplot as plt

#rutas que necesito

route_municipalities = "Lugares/"
json_salary_cuba = "Datos_Adicionales/salarios_cuba.json"
json_salary_world = "Datos_Adicionales/salarios_mundo.json"

#funcion que crea el DataFrame:
def load_df(route_municipalities):
    restaurants = []
    for municipality in os.listdir(route_municipalities):
        municipalities_path = os.path.join(route_municipalities, municipality)
        for place in os.listdir(municipalities_path):
            if place.endswith(".json"):
                with open (os.path.join(municipalities_path, place), "r", encoding = "utf-8") as f:
                    data = json.load(f)
                    restaurants.append(data)
                    data['municipality']= municipality
    df = pd.DataFrame(restaurants)
    column_municipality = df.pop("municipality")
    df.insert(1, "municipality", column_municipality)
    return df

#funcion para filtrar el dataframe por un municipio
def filter_restaurant(municipality):
    df = load_df(route_municipalities)
    filtered_df = df[df['municipality'] == municipality]
    return filtered_df

#funcion para mostrar las profesiones con el salario
def show_professions_salary(json_salary_cuba):
    with open(json_salary_cuba, "r", encoding = "utf-8") as file:
        data = json.load(file)
        dataframe = pd.DataFrame(list(data.items()), columns=['Profesión', 'Salario'])
        return dataframe
        
#función para verificar si un restaurante tiene todas las categorías del menú
def has_all_categories(menu):
    required_categories = ["appetizer", "main_course", "garrison", "desserts", "drinks"]
    for category in required_categories:
        if category not in menu or not menu[category]:
            return False
    return True

#función para crear la gráfica de pastel que muestre el pprciento que tienen los menus completos
def plot_menu_categories_pie_chart(df, municipality):
    df['has_all_categories'] = df['menu'].apply(has_all_categories)
    category_counts = df['has_all_categories'].value_counts()
    plt.figure(figsize=(3,4))
    plt.pie(category_counts, labels=['Tiene platos en todas las categorias', 'No tiene platos en al menos una categoria'], autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff6666'])
    plt.title(f'Porcentaje de restaurantes en {municipality} con todas las categorías del menú')
    plt.axis('equal')
    plt.show()

#función para contar el número de restaurantes que tienen una categoría específica
def count_restaurants_per_category(df, category):
    count = 0
    for i, row in df.iterrows():
        if category in row['menu'] and row['menu'][category]:
            count += 1
    return count

#función para crear el gráfico de barras para comparar las categorías entre municipios todo lindon
def plot_category_comparison_for_municipalities(df):
    categories = ["appetizer", "main_course", "garrison", "desserts", "drinks"]
    municipalities = ["Playa", "Diez de Octubre", "Centro Habana"]
    data = {}
    for municipality in municipalities:
        data[municipality] = []
        df_municipality = filter_restaurant(municipality)
        for category in categories:
            category_count = count_restaurants_per_category(df_municipality, category)
            data[municipality].append(category_count)
    category_counts_df = pd.DataFrame(data, index=categories)
    ax = category_counts_df.plot(kind='bar', figsize=(10,6), colormap='viridis')
    plt.title('Número de restaurantes que tienen cada categoría por municipio')
    plt.xlabel('Categoría del menú')
    plt.ylabel('Número de restaurantes')
    plt.xticks(rotation=45)
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', fontsize=10, color='black', xytext=(0, 6), textcoords='offset points')
    plt.tight_layout()
    plt.show()

#función para filtrar los restaurantes por municipio y las categorías
def filter_restaurants_by_categories(df, municipalities, categories):
    filtered_restaurants = []
    for municipality in municipalities:
        df_municipality = df[df['municipality'] == municipality]
        for i, row in df_municipality.iterrows():
            menu = row['menu']
            if categories['drinks'] in menu and categories['main_course'] in menu:
                if menu[categories['drinks']] and menu[categories['main_course']]:
                    filtered_restaurants.append(row)
    filtered_df = pd.DataFrame(filtered_restaurants)
    return filtered_df

#funcion para hallar el precio promedio de una comida
def find_average_price_main_course(df, municipality):
    df_municipality = df[df['municipality'] == municipality]
    average = 0
    count = 0
    for i, row in df_municipality.iterrows():
        menu = row['menu']
        if 'main_course' in menu:
            for dish in menu['main_course']:
                average += dish['price']
                count += 1
    if count > 0:
        average_price = average / count
    else:
        average_price = 0
    return average_price
