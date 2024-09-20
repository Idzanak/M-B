import folium
from folium import TileLayer
from folium.plugins import MousePosition

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
    tiles='https://raw.githubusercontent.com/Idzanak/M-B/main/tileset/{z}/{x}/{y}.png',  # URL или путь к вашему фоновому изображению
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

# Создание словаря
dict = {"label" : "Кальрадия",
        "select_all_checkbox": "Un/select all",
        "children": []
        }

# Сохраняем карту в HTML файл
map_obj.save('docs/map.html')