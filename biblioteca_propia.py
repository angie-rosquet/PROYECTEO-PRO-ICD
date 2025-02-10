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
    return pd.DataFrame(restaurants_s)

#funcion para mostrar las profesiones con el salario
def show_professions_salary(json_salary_cuba):
    with open(json_salary_cuba, "r", encoding = "utf-8") as file:
        data = json.load(file)
        dataframe = pd.DataFrame(list(data.items()), columns=['Profesión', 'Salario'])
        return dataframe

# funcion para mostrar el nombre:
def filter_restaurants_name():
    all_rest = []
    rest = load_all(route_municipality)
    all_rest.extend(rest['name'])
    df = pd.DataFrame(all_rest)
    return df

#funcion para calcular el promedio de la comida
def prom_meal(restaurant):
    price = 0
    count = 0 
    for meal in 