import json
import requests
from dotenv import load_dotenv
import os
import folium
from geopy import distance as dist

APIKEY = os.getenv('apikey')

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
    return float(lon), float(lat)


def main():
    load_dotenv()
    
    first_place = input('Где вы находитесь?:')
    first_cords = fetch_coordinates(address=first_place, apikey=APIKEY)
    if not first_cords:
        print("Не удалось найти ваше местоположение.")
        return
    
    user_lon, user_lat = first_cords
    
    with open("coffee.json", "r", encoding="CP1251") as my_file:
        capitals_json = my_file.read()

    spisok = []
    capitals = json.loads(capitals_json)
    
    for step in capitals:
        spis_cafe = dict()
        spis_cafe['title'] = step['Name']
        geo_cafe = step['geoData']['coordinates']
        spis_cafe['latitude'] = geo_cafe[1]
        spis_cafe['longitude'] = geo_cafe[0]
        distance = dist.distance((user_lat, user_lon), (geo_cafe[1], geo_cafe[0])).km
        spis_cafe['distance'] = distance
        spisok.append(spis_cafe)

    spisok_sorted = sorted(spisok, key=lambda x: x['distance'])

    closest_shops = spisok_sorted[:5]

    map_center = [user_lat, user_lon]
    map_zoom = 13 
    map = folium.Map(location=map_center, zoom_start=map_zoom)

    folium.Marker(
        location=[user_lat, user_lon],
        popup=f"Ваше местоположение: {first_place}",
        icon=folium.Icon(color='blue', icon='user'),
    ).add_to(map)

    for shop in closest_shops:
        folium.Marker(
            location=[shop["latitude"], shop["longitude"]],
            popup=f"{shop['title']} ({shop['distance']:.2f} км)",
            icon=folium.Icon(color='green', icon='coffee', prefix='fa'),
        ).add_to(map)

    map.save("coffee_shops_map.html")


if __name__ == '__main__':
    main()
