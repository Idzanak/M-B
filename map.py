import folium
from xml_data_parser import (
    locations, ru_locations, scale_coordinates, print_tree, towns, ru_factions, en_factions
)
from folium import TileLayer
from folium.plugins.treelayercontrol import TreeLayerControl
from folium.features import Marker
from folium.plugins import MousePosition
from folium.plugins import TagFilterButton


# Границы и координаты для корректировки
map_min_lat = -112
map_max_lat = 0
map_min_lon = 0
map_max_lon = 152
data_min_lat = 62.205 + 25
data_max_lat = 610.56 + 20
data_min_lon = 76.51701 - 15
data_max_lon = 782.63 + 15


# Создаем пустую карту
map_obj = folium.Map(location=[map_min_lat/2, map_max_lon/2],
                     zoom_start=4,
                     tiles=None,
                     crs='Simple',
                     min_lon=map_min_lon,
                     max_lon=map_max_lon,
                     min_lat=map_min_lat,
                     max_lat=map_max_lat,
                     height="100%",
                     width="100%",
                     max_bounds=True,
                     minZoom=3,
                     maxZoom=7,
                     control=False,
                     style = {'backgroundColor': 'black'}
                     )

# Добавляем на карту слой
TileLayer(
    tiles='tileset/{z}/{x}/{y}.png',
    attr='M&B Map tile set',
    overlay=False,
    show=True,
    no_wrap=True,
).add_to(map_obj)

factions_group = folium.FeatureGroup(name='Фракции', show=True).add_to(map_obj)
town_group = folium.FeatureGroup(name='Города', show=True).add_to(map_obj)
castle_group = folium.FeatureGroup(name='Замки', show=False).add_to(map_obj)
village_group = folium.FeatureGroup(name='Деревни', show=False).add_to(map_obj)
other_group = folium.FeatureGroup(name='Другое', show=False).add_to(map_obj)

Map_data = {"label" : "Кальрадия", "children": []}


Map_data['children'] = []





print(Map_data)
#print(Map_data)
#TagFilterButton(filter_list).add_to(map_obj)
TreeLayerControl(overlay_tree=Map_data).add_to(map_obj)
# Сохраняем карту в HTML файл

map_obj.save('docs/map.html')