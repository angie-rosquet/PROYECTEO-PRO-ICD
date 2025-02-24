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
        elif len(menu[category]) == 0:
            return False   
        elif len(menu[category]) == 1 and menu[category][0] == None:
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
            if len(row['menu'][category]) == 1 and row['menu'][category][0] == None:
                continue
            elif len(row['menu'][category]) == 0:
                continue
            else:
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
                    if len(menu[categories['drinks']]) != 0 or len(menu[categories['main_course']]) != 0:
                        if menu[categories['drinks']][0] != None and menu[categories['main_course']][0] != None:
                            filtered_restaurants.append(row)   
    filtered_df = pd.DataFrame(filtered_restaurants)
    return filtered_df

#funcion para hallar el precio promedio de un plato principal
def find_average_price_main_course(df, municipalities):
    average = 0
    count = 0
    for municipality in municipalities:
        df_municipality = df[df['municipality'] == municipality]
        for i, row in df_municipality.iterrows():
            menu = row['menu']
            if 'main_course' in menu:
                for dish in menu['main_course']:
                    if dish['price'] in dish and type(dish['price']) != float and int:
                        continue
                    else:
                        average += dish['price']
                        count += 1
    if count > 0: 
        average_price = average / count
    else:
        average_price = 0
    return round(average_price)

#funcion para hallar el precio promedio de una bebida
def find_average_price_drinks(df, municipalities):
    average = 0
    count = 0
    for municipality in municipalities:
        df_municipality = df[df['municipality'] == municipality]
        for i, row in df_municipality.iterrows():
            menu = row['menu']
            if 'drinks' in menu:
                for dish in menu['drinks']:
                    if dish['price'] in dish and type(dish['price']) != float and int:
                        continue
                    elif dish['price'] is None:
                        continue
                    else:
                        average += dish['price']
                        count += 1
    if count > 0: 
        average_price = average / count
    else:
        average_price = 0
    return round(average_price)

#funcion para hacer una grafica de barras q muestre el precio promedio de una comida en un restaurante
def prom_per_restaurante(df, restaurant):
    df_restaurant = df[df['name'] == restaurant]
    restaurant = df_restaurant.iloc[0]
    menu = restaurant['menu']
    mc = 0
    d = 0
    count = 0
    if 'main_course' in menu:
        for dish in menu['main_course']:
            if dish is not None and isinstance(dish['price'], (int, float)):
                mc += dish['price']
                count += 1
        if count > 0:
            mc = mc / count
    if 'drinks' in menu:
        for dish in menu['drinks']:
            if dish is not None and isinstance(dish['price'], (int, float)):
                d += dish['price']
                count += 1
        if count > 0:
            d = d / count
    return round(mc + d)
        
#funcion para crear una lista de nombres de restaurantes 
def restuarant_names_list(df, municipality):
    names = []
    df_municipality = df[df['municipality'] == municipality]
    for i, row in df_municipality.iterrows():
        row = row['name']
        names.append(row)
    return names

#funcion para tener una lista de promedios de una lista de restaurantes
def find_prom_price_for_restaurants_list(df, restaurant_names):
    prom_prices = []
    for restaurant_name in restaurant_names:
        data = prom_per_restaurante(df, restaurant_name)
        prom_prices.append(data)
    return prom_prices

#función para generar el gráfico de barras con los precios promedio de los restaurantes
def plot_prom_prices_for_restaurants(restaurant_names, prom_prices):
    plt.figure(figsize=(10, 6))
    bars = plt.bar(restaurant_names, prom_prices, color='#dd1313')
    plt.title('Precio Promedio de una Comida en Restaurantes')
    plt.xlabel('Restaurantes')
    plt.ylabel('Precio Promedio')
    plt.xticks(rotation=45, ha='right')
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 0.1, f'{height:.2f}', ha='center', fontsize=10)
    plt.tight_layout()
    plt.show()

#funcion para mostrar el menu de un restaurante
def show_menu(df, restaurant):
    df_restaurant = df[df['name'] == restaurant]
    menu = df_restaurant.iloc[0]['menu']
    menu_filtered = {}
    if 'main_course' in menu:
        menu_filtered['main_course'] = menu['main_course']
    if 'drinks' in menu:
        menu_filtered['drinks'] = menu['drinks']
    return menu_filtered

#funcion para filtrar un dataframe pero que no tenga en cuenta la fila que tenga unos nombres especificos de restaurantes
def filter_restaurants_not_name(df, municipality,restaurants_list):
    filtered_restaurants = []
    df_municipality = df[df['municipality'] == municipality]
    for _, row in df_municipality.iterrows():
        if row['name'] not in restaurants_list:
            filtered_restaurants.append(row)
    filtered_df = pd.DataFrame(filtered_restaurants)
    return filtered_df

#funcion para graficar que tanto por ciento representa del salario de cuba una precio establecido 
def plot_salary_percentage(json_salary_cuba, prom, label):
    percentages = []
    with open(json_salary_cuba, "r", encoding = "utf-8") as f:
        json_salaries = json.load(f)
        professions = list(json_salaries.keys())
        salaries = list(json_salaries.values())
        for salary in salaries:
            if salary != 0:
                percentages.append((prom / salary) * 100) 
        plt.figure(figsize=(10, 6))
        plt.bar(professions, percentages, color='#2c9b0d')
        plt.title(f'Porcentaje del salario que representa el precio de una comida promedio para cada profesion en {label}')
        plt.xlabel('Profesiones')
        plt.ylabel('Porcentaje (%)')
        for i, value in enumerate(percentages):
            plt.text(i, value + 0.5, f'{value:.2f}%', ha='center', fontsize=10)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout() 
        plt.show()
        
#funciion para hallar el plato mas barato de un restaurante 
def find_cheap_price_restaurant(df, restaurant, category):
    dish = {"name": "", "price": 1000000}
    df_restaurant = df[df['name'] == restaurant]
    if df_restaurant.shape[0] == 0:
        return "Restaurante no encontrado"
    if 'menu' in df_restaurant.columns:
        menu = df_restaurant.iloc[0]['menu']
        
        if category in menu:
            for row in menu[category]:
                if row is not None and isinstance(row, dict) and 'price' in row:
                    if row['price'] < dish['price']:
                        dish['name'] = row['name']
                        dish['price'] = row['price']
    return dish

#funcion para hacer una grafica por municipios que muestre el precio promedio de una comida 
def plot_prom_price_for_municipalities(df, municipalities):
    x = []
    y = []
    for municipality in municipalities:
        x.append(municipality)
        mc = find_average_price_main_course(df, [municipality])
        d = find_average_price_drinks(df, [municipality])
        total = mc + d
        y.append(total)
    plt.figure(figsize=(10, 6))
    plt.bar(x, y, color='#912b84')
    plt.title('Promedio de una comida por municipios')
    plt.xlabel('Municipios')
    plt.ylabel('Precio Promedio')
    for i, value in enumerate(y):
        plt.text(i, value + 0.5, f'{value:.2f}', ha='center', fontsize=10)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout() 
    plt.show()

#funcion diccionario
def dic_generator (json_route):
    with open (json_route, 'r', encoding = 'utf=8') as f:
        data = json.load(f)
        return data

#funcion para calcular cuanto ganan por dia
def calculate_daily_salary(json_salary_cuba, profession):
    if profession == "pensionado":
        pass
    if profession in json_salary_cuba:
        monthly_salary = json_salary_cuba[profession]
        daily_salary = monthly_salary / 20  # Suponiendo que trabajan 20 días al mes
        return daily_salary

#funcion para calcular la cantidad de horas que debe trabajar alguien 
def calculate_working_hours_for_food(json_salary_cuba, avg_food_price):
    professions = ["médico", "profesor", "científico o investigador titular", "periodista", "chofer", "salario promedio"]
    working_hours = []
    for profession in professions:
        daily_salary = calculate_daily_salary(json_salary_cuba, profession)
        if daily_salary is not None:
            hours_needed = (avg_food_price / daily_salary) * 8  # Horas necesarias para cubrir el precio de la comida
            working_hours.append(hours_needed)
    return working_hours

#funcion de la grafica de esa vaina de las horas
def plot_working_hours_by_profession(json_salary, avg_food_price):
    working_hours = calculate_working_hours_for_food(json_salary, avg_food_price)
    profession = ["médico", "profesor", "científico o investigador titular", "periodista", "chofer", "salario promedio"]
    plt.figure(figsize=(10, 6))
    bars = plt.bar(profession, working_hours, color='skyblue')
    plt.title('Horas de trabajo necesarias para cubrir el precio de una comida')
    plt.xlabel('Profesión')
    plt.ylabel('Horas de trabajo necesarias')
    plt.xticks(rotation=45, ha='right')
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height + 0.1, f'{height:.2f}', ha='center', fontsize=10)
    plt.tight_layout()  # Ajustar el layout para evitar que los textos se corten
    plt.show()

#funcion para hacer una grafica por municipios que muestre el precio promedio de una comida en dolares
def plot_prom_price_for_municipalities_inter(df, municipalities):
    x = []
    y = []
    for municipality in municipalities:
        x.append(municipality)
        mc = find_average_price_main_course(df, [municipality])
        d = find_average_price_drinks(df, [municipality])
        total = mc + d
        y.append(total/340)
    plt.figure(figsize=(10, 6))
    plt.bar(x, y, color='#912b84')
    plt.title('Promedio de una comida por municipios')
    plt.xlabel('Municipios')
    plt.ylabel('Precio Promedio')
    for i, value in enumerate(y):
        plt.text(i, value + 0.5, f'{value:.2f}', ha='center', fontsize=10)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout() 
    plt.show()
    
#funcion para hacer una lista por municipios que muestre el precio promedio de una comida en dolares
def prom_municipality_in_dolar(df, municipalities):
    data = {} 
    for municipality in municipalities:
        mc = find_average_price_main_course(df, [municipality])
        d = find_average_price_drinks(df, [municipality])
        total = (mc + d) / 340
        data[municipality] = total
    return data

#funcion para filtrar el pais en el json
def get_salaries_by_country(json_salary_data, country):
    with open (json_salary_world, 'r', encoding ='utf8') as f:
        data = json.load(f)
        if country in data:
            lol = data[country]
            return lol
    

#funcion para calcular que tanto por ciento representa una comida en el salario del pais que elija
def percentage(country, profession, municipalities):
    country_salaries = get_salaries_by_country(json_salary_world, country)
    if profession not in country_salaries:
        return f"La profesión {profession} no se encuentra en los datos de {country}"
    salary = country_salaries[profession]
    data = prom_municipality_in_dolar(load_df(route_municipalities), municipalities)
    percentages = {}
    for municipality, avg_food_price in data.items():
        percentage = (avg_food_price / salary) * 100
        percentages[municipality] = round(percentage, 2)
    return percentages


def plot_salary_percentage_for_profession_in_municipalities(df, json_salary_world, profession, municipalities):
    countries = ["Estados Unidos", "Uruguay", "Cuba"]
    plt.figure(figsize=(10, 6))
    for country in countries:
        country_salaries = get_salaries_by_country(json_salary_world, country)
        
        if profession not in country_salaries:
            print(f"La profesión {profession} no se encuentra en los datos de {country}")
            return
        salary = country_salaries[profession]
        data = prom_municipality_in_dolar(df, municipalities)
        percentages = {}
        for municipality, avg_food_price in data.items():
            if salary > 0:  # Evitar división por cero
                percentage = (avg_food_price / salary) * 100
                percentages[municipality] = round(percentage, 2)
            else:
                percentages[municipality] = 0
        if not percentages:
            print(f"No se calcularon porcentajes para {country}. Puede que algunos valores de comida estén vacíos.")
            return
        plt.plot(list(percentages.keys()), list(percentages.values()), label=country, marker='o')
    plt.title(f'Porcentaje de lo que equivale una cena en estos municipios con respecto al salario de {profession}')
    plt.xlabel('Municipios')
    plt.ylabel('Porcentaje (%)')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.show()