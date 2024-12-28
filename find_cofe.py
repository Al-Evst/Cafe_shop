import json
import requests
from dotenv import load_dotenv
import os
import folium


def fetch_coordinates(address, apikey=None):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def main():
    load_dotenv()
    APIKEY = os.getenv('apikey')
    
    with open("C:/Python_study/cafe_map/coffee.json", "r", encoding="CP1251") as my_file:
        capitals_json = my_file.read()

    spisok = []

    capitals = json.loads(capitals_json)
    for step in capitals:
        spis_cafe = dict()
        spis_cafe['title'] = step['Name']
        geo_cafe = step['geoData']['coordinates']
        spis_cafe['latitude'] = geo_cafe[1]
        spis_cafe['longitude'] = geo_cafe[0]
        spisok.append(spis_cafe)

    map_center = [geo_cafe[1], geo_cafe[0]]
    map_zoom = 10
    map = folium.Map(location=map_center, zoom_start=map_zoom)

    for shop in spisok[:5]:
        folium.Marker(
            location=[shop["latitude"], shop["longitude"]],
            popup=shop["title"],
            icon=folium.Icon(color='blue', icon='cloud'),
        ).add_to(map)

    map.save("coffee_shops_map.html")


if __name__ == '__main__':
    main()