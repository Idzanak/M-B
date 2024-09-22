import xml.etree.ElementTree as ET
import re

root = ET.parse('XML game data/settlements.xml').getroot()
root_ru = ET.parse('XML game data/std_settlements_xml_rus.xml').getroot()
lang = 'ru'

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

def remove_braces_text(text):
    pattern = r"\{.*?\}"
    result = re.sub(pattern, "", text)
    return result

def print_tree(data, indent=0):
    """ Рекурсивно выводит словарь и списки в виде дерева. """
    spacing = ' ' * indent  # Задаем отступ
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{spacing}{key}:")
            print_tree(value, indent + 4)  # Увеличиваем отступ для вложенных элементов
    elif isinstance(data, list):
        for i, item in enumerate(data):
            print(f"{spacing}[{i}]:")
            print_tree(item, indent + 4)  # Увеличиваем отступ для вложенных элементов
    else:
        print(f"{spacing}{data}")  # Для остальных типов, просто выводим значение

def text_translate(data, language='ru'):
    if language == 'ru':
        for ru_keys in root_ru.find('strings'):
            if data.split('}')[0].split('=')[1] == ru_keys.get('id'):
                 return remove_braces_text(ru_keys.get('text'))
    else:
        return remove_braces_text(data)


#Создание списка всех локаций
locations=[]
ru_locations = []
for settlements in root:
    location = {'id': settlements.attrib['id'],
                'coords': [scale_coordinates(float(settlements.attrib['posY']), float(settlements.attrib['posX']))],
                'name': settlements.attrib['name'],
                'type': settlements[0][0].tag}
    if 'text' in settlements.attrib: location['text'] = settlements.attrib['text']
    if settlements.findall("./Components/Town"):
        if settlements[0][0].attrib['is_castle'] == 'true': location['type'] = 'Castle'
        else: location['type'] = 'Town'
        location['is_castle'] = settlements[0][0].attrib['is_castle']
        location['clan'] = settlements.attrib['owner'].replace('Faction.','')
        location['faction'] = settlements.attrib['owner'].replace('Faction.clan_','').rsplit('_', 1)[0]
        location['level'] = settlements[0][0].attrib['level']
        location['prosperity'] = settlements[0][0].attrib['prosperity']
    if settlements.findall("./Components/Village"):
        location['bound'] = settlements[0][0].attrib['bound'].replace('Settlement.', '')
        location['village_type'] = settlements[0][0].attrib['village_type']
        location['hearth'] = settlements[0][0].attrib['hearth']
    locations.append(location)
    ru_locations.append(location.copy())
    del location

for i in range(len(locations)): # Перевод русского списка и
    if 'text' in locations[i]:
        ru_locations[i]['text'] = text_translate(locations[i]['text'])
        locations[i]['text'] = text_translate(locations[i]['text'],'en')
    if 'name' in locations[i]:
        ru_locations[i]['name'] = text_translate(locations[i]['name'])
        locations[i]['name'] = text_translate(locations[i]['name'], 'en')

towns = [d for d in ru_locations if d.get('type')=='Town']
villages = [d for d in ru_locations if d.get('type')=='Village']
castles = [d for d in ru_locations if d.get('type')=='Castle']
hideouts = [d for d in ru_locations if d.get('type')=='Hideout']
