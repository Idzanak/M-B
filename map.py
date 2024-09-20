import folium
from folium import TileLayer
from folium.plugins.treelayercontrol import TreeLayerControl
from folium.features import Marker
from folium.plugins import MousePosition
import xml.etree.ElementTree as ET
import re

root = ET.parse('XML game data/settlements.xml').getroot()
root_ru = ET.parse('XML game data/std_settlements_xml_rus.xml').getroot()
lang = 'ru'  # Выбираем язык для данных 'ru' для русского, любое другое значение для анг

# Границы карты
map_min_lat = -112
map_max_lat = 0
map_min_lon = 0
map_max_lon = 152

# Границы координат для корректировки
data_min_lat = 62.205 + 25
data_max_lat = 610.56 + 20
data_min_lon = 76.51701 - 15
data_max_lon = 782.63 + 15

def scale_coordinates(lat, lon):
    # Масштабирование широты
    scaled_lat = map_min_lat + (lat - data_min_lat) * (map_max_lat - map_min_lat) / (data_max_lat - data_min_lat)
    # Масштабирование долготы
    scaled_lon = map_min_lon + (lon - data_min_lon) * (map_max_lon - map_min_lon) / (data_max_lon - data_min_lon)
    return [scaled_lat, scaled_lon]

# Создаем карту с пустым фоном
map_obj = folium.Map(location=[map_min_lat/2, map_max_lon/2], zoom_start=3, tiles=None, crs='Simple', min_lon=map_min_lon, max_lon=map_max_lon, min_lat=map_min_lat, max_lat=map_max_lat, height="100%", width="100%", max_bounds=True)

TileLayer(
    tiles='tileset/{z}/{x}/{y}.png',  # URL или путь к вашему фоновому изображению
    attr='M&B Map tileset',  # Атрибуция (может быть пустой для вашего проекта)
    name='M&B Map',
    overlay=False,
    control=False,
    show=True,
    minZoom=3,
    maxZoom=7,
    no_wrap=True,
).add_to(map_obj)

town_group = folium.FeatureGroup(name='Города', show=True).add_to(map_obj)
castle_group = folium.FeatureGroup(name='Замки', show=False).add_to(map_obj)
village_group = folium.FeatureGroup(name='Деревни', show=False).add_to(map_obj)
other_group = folium.FeatureGroup(name='Другое', show=False).add_to(map_obj)
folium.LayerControl().add_to(map_obj)

# Определение списка фракций
factions = set()
for settlements in root:
    if 'owner' in settlements.attrib:
        factions.add(settlements.attrib['owner'].split('.')[1].split('_', 1)[1].rsplit('_', 1)[0])

# Создание словаря

dict = {"label" : "Кальрадия",
        "select_all_checkbox": "Un/select all",
        "children": []
        }
for faction in factions:
    for location in root:
        if 'owner' in location.attrib:
            location_temp_data = {}
            if faction == location.attrib['owner'].split('.')[1].split('_', 1)[1].rsplit('_', 1)[0]:
                location_temp_data["label"] = location.attrib['id']
        dict["children"].append({"label": faction, "select_all_checkbox": True, "children": []})

for i, k in dict.items():
    print(i, k)

TreeLayerControl(overlay_tree=dict).add_to(map_obj)
# Сохраняем карту в HTML файл
map_obj.save('docs/map.html')