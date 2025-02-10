import pandas as pd
import json
import os

#rutas que necesito

route_municipality = "Lugares/"
json_salary_cuba = "Datos_Adicionales/salarios_cuba.json"
json_salary_world = "Datos_Adicionales/salarios_mundo.json"

#funcion para saber de que municipio es
def extract_municipio(address):
    return address.split(",")[-1].strip()

#funcion que crea el DataFrame:
def load_all(route_municipality):
    restaurants = []
    restaurants_df = 0
    for municipality in os.listdir(route_municipality):
        municipality_path = os.path.join(route_municipality, municipality)
        if os.path.isdir(municipality_path):
            for place in os.listdir(municipality_path):
                if place.endswith(".json"):
                    place_path = os.path.join(municipality_path, place)
                    with open (place_path, "r", encoding = "utf-8") as file:
                        data = json.load(file)
                        restaurants.append(data)
    restaurants_df = pd.DataFrame(restaurants)
    return restaurants_df

#funcion para crear un DataFrame en dependencia del municipio elegido
def load_for_municipality(municipality):
    restaurants_s = []
    municipality_route = os.path.join(route_municipality, municipality)
    for place in os.listdir(municipality_route):
        if place.endswith(".json"):
            with open (os.path.join(municipality_route, place), "r", encoding = "utf-8") as file:
                data = json.load(file)
                restaurants_s.append(data)
    df = pd.DataFrame(restaurants_s)
    return df

#funcion para mostrar las profesiones con el salario
def show_professions_salary(json_salary_cuba):
    with open(json_salary_cuba, "r", encoding = "utf-8") as file:
        data = json.load(file)
        dataframe = pd.DataFrame(list(data.items()), columns=['Profesión', 'Salario'])
        return dataframe

#funcion que calcula cuanto pagan por hora(44 horas al mes)
def pay_h(profession):
    with open(json_salary_cuba, "r", encoding = "utf-8") as f:
        data = json.load(f)
        data = data.get(profession)
        horas = data / 176
        return round(horas, 2)

# funcion para mostrar el nombre:
def filter_restaurants_name():
    all_rest = []
    rest = load_all(route_municipality)
    all_rest.extend(rest['name'])
    df = pd.DataFrame(all_rest)
    return df

#lista de nombres de restaurantes en dependencia del municipio(para la grafica)
def rest_per_municipality(municipality):
    rest = []
    mun = os.path.join(route_municipality, municipality)
    for place in os.listdir(mun):
        if place.endswith(".json"):
            with open (os.path.join(mun, place), "r", encoding = "utf-8") as file:
                data = json.load(file)
                rest.append(data["name"])
    return rest

#funcion para comida promedio de un restaurante
def prom_category(restaurant):
    with open(restaurant, 'r', encoding='utf-8') as f:
        restaurant = json.load(f)
    prom = []
    total = 0
    categorias = ['appetizer', 'main_course', 'garrison', 'desserts', 'drinks']
    for categoria in categorias:
        items = restaurant['menu'].get(categoria, {})
        if len(items) > 0:
            for item in items:
                if item and 'price' in item and isinstance(item['price'], (int, float)):  # Validar item antes de acceder
                    total += item['price']
            prom.append(total / len(items))
        else:
            prom.append(0)
        return round(sum(prom))
    
def list_prom(municipality):
    list1 = []
    route = os.path.join(route_municipality, municipality)
    for place in os.listdir(route):
        a = prom_category(os.path.join(route, place))
        list1.append(a)
    return list1
    
def prom_mun(municipality):
    list1 = []
    list2 = []
    route = os.path.join(route_municipality, municipality)
    categories = ['appetizer', 'main_course', 'garrison', 'desserts', 'drinks']
    for c in categories:
        list1 = []
        for place in os.listdir(route):
            with open(os.path.join(route, place), encoding="utf-8") as f:
                data = json.load(f)
                if c in data['menu']:
                    if not isinstance(data['menu'][c], bool):
                        precios = [int(item["price"]) for item in data['menu'][c] if isinstance(item, dict) and "price" in item and item["price"] is not None]
                        list1.extend(precios)
                promedio = sum(list1) / len(list1) if list1 else 0
            list2.append(promedio)
        return round(sum(list2))
