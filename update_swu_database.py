import requests
import csv
import time
import json
from datetime import datetime

today = datetime.today().strftime('%Y_%m_%d')
print(today)

swu_sets = ['sor','shd','twi']
all_cards_dict = {}
for swu_set in swu_sets:
    url = f'https://api.swu-db.com/cards/{swu_set}'
    response = requests.get(url)
    if response.status_code == 200:
        card_data = response.json()

        with open(f'E:/StarWarsUnlimited/data/all_card_data_{swu_set}.json', 'w') as file:
            json.dump(card_data, file, indent=4)
        with open(f'E:/StarWarsUnlimited/data/data_archive/all_card_data_{swu_set}_{today}.json', 'w') as file:
            json.dump(card_data, file, indent=4)

        for i in card_data['data']:
            set_code = i['Set'].lower()
            number = i['Number']
            all_cards_dict[f"{set_code}_{number}"] = i

with open(f'E:/StarWarsUnlimited/data/all_card_data.json', 'w') as file:
    json.dump(all_cards_dict, file, indent=4)
with open(f'E:/StarWarsUnlimited/data/data_archive/all_card_data_{today}.json', 'w') as file:
    json.dump(all_cards_dict, file, indent=4)


with open('E:/StarWarsUnlimited/data/all_card_data.json', 'r') as file:
    all_cards = json.load(file)

card_count = 0
full_collection_detailed = []
normal_collection_jsons = []
for k,v in all_cards.items():
    if v["VariantType"] == "Normal": normal_collection_jsons.append(v)


for card_data in normal_collection_jsons:
    count = 1
    set = card_data.get('Set').lower()
    number = card_data.get('Number')
    name = card_data.get('Name')
    subtitle = card_data.get('Subtitle')
    card_type = card_data.get('Type')
    aspects = card_data.get('Aspects')
    traits = card_data.get('Traits')
    if traits is not None:
        for i in traits: i = i.replace("TWI'LEK", "TWILEK")
    arenas = card_data.get('Arenas')
    cost = card_data.get('Cost')
    power = card_data.get('Power')
    hp = card_data.get('HP')
    fronttext = card_data.get('FrontText')
    if fronttext is not None: fronttext = fronttext.replace("TWI'LEK", "TWILEK")
    backtext = card_data.get('BackText')
    if backtext is not None: backtext = backtext.replace("TWI'LEK", "TWILEK")
    epicaction = card_data.get('EpicAction')
    doublesided = card_data.get('DoubleSided')
    backart = card_data.get('BackArt')
    frontart = card_data.get('FrontArt')
    rarity = card_data.get('Rarity')
    marketprice = card_data.get('MarketPrice')
    karabast_number = number

    not_repeat_special = True

    if rarity == "Special": not_repeat_special = False
    # THIS Code is to include Unique special cards from the starter decks but it seems most people don't want that so I've replaced it for now with the line of code directly above
    # if rarity == "Special": 
        # for row in full_collection_detailed:
        #     (pre_name, pre_subtitle,pre_count,pre_card_type, pre_aspects, pre_traits,pre_arenas,pre_cost,pre_power,pre_hp) = row[2:12]
        #     if (name,subtitle,card_type,aspects,traits,arenas,cost,power,hp) == (pre_name, pre_subtitle,pre_card_type, pre_aspects, pre_traits,pre_arenas,pre_cost,pre_power,pre_hp): not_repeat_special = False

    row = [set, number,name,subtitle,count,card_type,aspects,traits,arenas,cost,power,hp,fronttext,backtext,epicaction,doublesided,backart,frontart,rarity,marketprice,karabast_number]
    card_count += 1

    if not_repeat_special: full_collection_detailed.append(row)

# GET SHOWCASE DATA
with open('E:/StarWarsUnlimited/data/all_card_data.json', 'r') as file:
    all_cards = json.load(file)

card_count = 0
showcase_detailed = []
showcase_jsons = []
for k,v in all_cards.items():
    if v["VariantType"] == "Showcase": showcase_jsons.append(v)

for i in showcase_jsons:
    normal_number = ''
    name = i['Name']
    subtitle = i['Subtitle']
    for card in normal_collection_jsons:
        if card['Name'] == name and card['Subtitle'] == subtitle: normal_number = card['Number']
    if normal_number != '': i['KarabastNumber'] = normal_number

for card_data in showcase_jsons:
    set = card_data.get('Set').lower()
    number = card_data.get('Number')
    name = card_data.get('Name')
    subtitle = card_data.get('Subtitle')
    card_type = card_data.get('Type')
    aspects = card_data.get('Aspects')
    traits = card_data.get('Traits')
    if traits is not None:
        for i in traits: i = i.replace("TWI'LEK", "TWILEK")
    arenas = card_data.get('Arenas')
    cost = card_data.get('Cost')
    power = card_data.get('Power')
    hp = card_data.get('HP')
    fronttext = card_data.get('FrontText')
    if fronttext is not None: fronttext = fronttext.replace("TWI'LEK", "TWILEK")
    backtext = card_data.get('BackText')
    if backtext is not None: backtext = backtext.replace("TWI'LEK", "TWILEK")
    epicaction = card_data.get('EpicAction')
    doublesided = card_data.get('DoubleSided')
    backart = card_data.get('BackArt')
    frontart = card_data.get('FrontArt')
    rarity = card_data.get('Rarity')
    marketprice = card_data.get('MarketPrice')
    karabast_number = card_data.get('KarabastNumber')

    row = [set, number,name,subtitle,count,card_type,aspects,traits,arenas,cost,power,hp,fronttext,backtext,epicaction,doublesided,backart,frontart,rarity,marketprice,karabast_number]
    card_count += 1
    print(f"{card_count}) {name} -- {number} | {karabast_number}")

    showcase_detailed.append(row)

# GET HYPERSPACE DATA
card_count = 0
hyperspace_detailed = []
hyperspace_jsons = []
for k,v in all_cards.items():
    if v["VariantType"] == "Hyperspace": hyperspace_jsons.append(v)

for i in hyperspace_jsons:
    normal_number = ''
    name = i['Name']
    subtitle = i.get('Subtitle')
    for card in normal_collection_jsons:
        if subtitle:
            if card['Name'] == name and card['Subtitle'] == subtitle: normal_number = card['Number']
        else: 
            if card['Name'] == name: normal_number = card['Number']
    
    if normal_number != '': i['KarabastNumber'] = normal_number
    else: print(f"ERROR: {i}")
for card_data in hyperspace_jsons:
    set = card_data.get('Set').lower()
    number = card_data.get('Number')
    name = card_data.get('Name')
    subtitle = card_data.get('Subtitle')
    card_type = card_data.get('Type')
    aspects = card_data.get('Aspects')
    traits = card_data.get('Traits')
    if traits is not None:
        for i in traits: i = i.replace("TWI'LEK", "TWILEK")
    arenas = card_data.get('Arenas')
    cost = card_data.get('Cost')
    power = card_data.get('Power')
    hp = card_data.get('HP')
    fronttext = card_data.get('FrontText')
    backtext = card_data.get('BackText')
    epicaction = card_data.get('EpicAction')
    doublesided = card_data.get('DoubleSided')
    backart = card_data.get('BackArt')
    frontart = card_data.get('FrontArt')
    rarity = card_data.get('Rarity')
    marketprice = card_data.get('MarketPrice')
    karabast_number = card_data.get('KarabastNumber')

    row = [set, number,name,subtitle,count,card_type,aspects,traits,arenas,cost,power,hp,fronttext,backtext,epicaction,doublesided,backart,frontart,rarity,marketprice,karabast_number]
    card_count += 1
    print(f"{card_count}) {name} -- {number} | {karabast_number}")

    hyperspace_detailed.append(row)

card_lists = [full_collection_detailed,showcase_detailed,hyperspace_detailed]
for card_list in card_lists:
    for card in card_list:
        fronttext = card[12]
        backtext = card[13]
        traits = card[7]
        if fronttext is not None:
            fronttext = fronttext.replace('\n', '|')
            fronttext = fronttext.replace("TWI'LEK", "TWILEK")
        if backtext is not None:
            backtext = backtext.replace('\n', '|')
            backtext = backtext.replace("TWI'LEK", "TWILEK")
        card[12] = fronttext
        card[13] = backtext
        if traits:
            for i in range(len(traits)):
                traits[i] = traits[i].replace("TWI'LEK", "TWILEK")
        card[7] = traits

# WRITE THE CSV FILES
header = [
    'set', 'number', 'name', 'subtitle', 'count', 'type', 
    'aspects', 'traits', 'arenas', 'cost', 'power', 'hp', 
    'fronttext', 'backtext', 'epicaction', 'doublesided', 
    'backart', 'frontart', 'rarity', 'marketprice','karabast_number'
]



with open (f'E:/StarWarsUnlimited/data/data_archive/FULL_collection_detailed_{today}.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(full_collection_detailed)

with open (f'E:/StarWarsUnlimited/data/FULL_collection_detailed.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(full_collection_detailed)

with open (f'E:/StarWarsUnlimited/data/data_archive/showcase_detailed_{today}.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(showcase_detailed)

with open (f'E:/StarWarsUnlimited/data/showcase_detailed.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(showcase_detailed)

with open (f'E:/StarWarsUnlimited/data/data_archive/hyperspace_detailed_{today}.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(hyperspace_detailed)

with open (f'E:/StarWarsUnlimited/data/hyperspace_detailed.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(hyperspace_detailed)


# COPY THE CSV FILES
import shutil


full_source = 'E:/StarWarsUnlimited/data/FULL_collection_detailed.csv'
full_destination1 = 'E:/StarWarsUnlimited/SWU_boosters/SWU_all_cards.csv'
full_destination2 = 'E:/StarWarsUnlimited/SWU_all_cards.csv'

shutil.copy(full_source, full_destination1)
shutil.copy(full_source, full_destination2)

print("Normal Collection File copied successfully.")

showcase_source = 'E:/StarWarsUnlimited/data/showcase_detailed.csv'
showcase_destination1 = 'E:/StarWarsUnlimited/SWU_boosters/SWU_showcase.csv'
showcase_destination2 = 'E:/StarWarsUnlimited/SWU_showcase.csv'

shutil.copy(showcase_source, showcase_destination1)
shutil.copy(showcase_source, showcase_destination2)

print("Showcase Collection File copied successfully.")

hyperspace_source = 'E:/StarWarsUnlimited/data/hyperspace_detailed.csv'
hyperspace_destination1 = 'E:/StarWarsUnlimited/SWU_boosters/SWU_hyperspace.csv'
hyperspace_destination2 = 'E:/StarWarsUnlimited/SWU_hyperspace.csv'

shutil.copy(hyperspace_source, hyperspace_destination1)
shutil.copy(hyperspace_source, hyperspace_destination2)

print("Hyperspace Collection File copied successfully.")