from flask import Flask, render_template, request, Response
import csv
import json
import random
import copy

app = Flask(__name__, template_folder='templates')


# Load the card collection from CSV
collection = []
with open('SWU_all_cards.csv', 'r', encoding='ISO-8859-1') as file:
    Reader = csv.reader(file)
    for line in Reader:
        collection.append(line)



full_card_pool = []

# Ensure each card appears in the pool according to its count in the collection
for c in collection[1:]:
    count = int(c[4])
    card = c[:4] + c[5:]
    for i in range(count):
        full_card_pool.append(card)

# This creates one booster pack according to the distribution rules
def get_booster(set='sor',qty = "1",):

    card_pool = {}
    packs = []
    
    index = 0
    for c in full_card_pool:
        if (set == 'any' and c[0] != 'twi') or c[0] == set:
            card_pool[index] = c
            index += 1


    leaders = {}
    bases = {}
    commons = {}
    uncommons = {}
    rares = {}
    legendaries = {}

    for i in range(int(qty)):

        pack = []
        for k, v in card_pool.items():
            if v[4] == 'Leader': leaders[k] = v
            elif v[4] == 'Base': bases[k] = v
            elif v[17] == 'Common': commons[k] = v
            elif v[17] == 'Uncommon': uncommons[k] = v
            elif v[17] == 'Rare': rares[k] = v
            elif v[17] == 'Legendary': legendaries[k] = v

        # 1 Leader, 1 Base, 9 Commons, 3 Uncommons, 1 Rare/Legendary, 1 random card
        leader_index = random.choice(list(leaders.keys()))
        leader = copy.deepcopy(card_pool[leader_index])
        leader.append('1 Leader')
        pack.append(leader)

        base_index = random.choice(list(bases.keys()))
        base = copy.deepcopy(card_pool[base_index])
        base.append('1 Base')
        pack.append(base)
        
        common_indeces = []
        for i in range(9):
            common_index = random.choice(list(commons.keys()))
            while common_index in common_indeces:
                common_index = random.choice(list(commons.keys()))
            common_indeces.append(common_index)

            common = copy.deepcopy(card_pool[common_index])
            common.append(f"{i+1} of 9 Commons")
            pack.append(common)
        
        uncommon_indeces = []
        for i in range(3):
            uncommon_index = random.choice(list(uncommons.keys()))
            while uncommon_index in uncommon_indeces:
                uncommon_index = random.choice(list(uncommons.keys()))
            uncommon_indeces.append(uncommon_index)
            
            uncommon = copy.deepcopy(card_pool[uncommon_index])
            uncommon.append(f"{i+1} of 3 Uncommons")
            pack.append(uncommon)

        random_number = random.randint(1, 8)
        if len(legendaries) > 0 and random_number == 8:
            rare_index = random.choice(list(legendaries.keys()))
        else:
            rare_index = random.choice(list(rares.keys()))
        rare = copy.deepcopy(card_pool[rare_index])
        rare.append("1 Rare or Legendary")
        pack.append(rare)

        any_card_index = random.choice(list(card_pool.keys()))
        any_card_type = card_pool[any_card_index][4]
        while any_card_type == 'Leader' or any_card_type == 'Base':
            any_card_index = random.choice(list(card_pool.keys()))
            any_card_type = card_pool[any_card_index][4]
        any_card = copy.deepcopy(card_pool[any_card_index])    
        any_card.append("1 'Foil' of any rarity")
        pack.append(any_card)
        packs.append(pack)
    return packs

@app.route('/')
def index():
    # Get the set and quantity for each booster from query parameters
    qty_sor = request.args.get('qty_sor', '0')
    qty_shd = request.args.get('qty_shd', '0')
    qty_twi = request.args.get('qty_twi', '0')

    # Generate booster packs based on quantities selected by the user
    boosters = []

    if int(qty_sor) > 0:
        boosters.extend(get_booster(set='sor', qty=qty_sor))
    if int(qty_shd) > 0:

        boosters.extend(get_booster(set='shd', qty=qty_shd))
    if int(qty_twi) > 0:
        boosters.extend(get_booster(set='twi', qty=qty_twi))

    # Render the HTML template with the booster packs and current set
    return render_template('booster_pack.html', boosters=boosters, swu_set='multiple')

@app.route('/generate_csv')
def generate_csv():
    # Get the booster packs from the request args
    qty_sor = request.args.get('qty_sor', '0')
    qty_shd = request.args.get('qty_shd', '0')
    qty_twi = request.args.get('qty_twi', '0')

    boosters = []
    if int(qty_sor) > 0:
        boosters.extend(get_booster(set='sor', qty=qty_sor))
    if int(qty_shd) > 0:
        boosters.extend(get_booster(set='shd', qty=qty_shd))
    if int(qty_twi) > 0:
        boosters.extend(get_booster(set='twi', qty=qty_twi))

    # Create CSV string
    csv_string = "set,number,name,subtitle,type,aspects,traits,arenas,cost,power,hp,fronttext,backtext,epicaction,doublesided,backart,frontart,rarity,marketprice\n"  # Header row
    for booster in boosters:
        for card in booster:
            fronttext = str(card[11]).replace(',', '')
            backtext = str(card[12]).replace(',', '')
            csv_string += f'{card[0]},\"{card[1]}\",\"{card[2]}\",\"{card[3]}\",\"{card[4]}\",\"{card[5]}\",\"{card[6]}\",\"{card[7]}\",\"{card[8]}\",\"{card[9]}\",\"{card[10]}\",\"{fronttext}\",\"{backtext}\",\"{card[13]}\",\"{card[14]}\",\"{card[15]}\",\"{card[16]}\",\"{card[17]}\",\"{card[18]}\"\n'  # Adjust columns as needed

    # Return the CSV as a response
    return Response(
        csv_string,
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=booster_packs.csv"}
    )

@app.route('/generate_json', methods=['POST'])
def generate_json():
    try:
        # Get the selected cards from the request JSON
        data = request.get_json()
        
        # Check if the data is valid
        if not data or 'deck' not in data:
            return Response("Invalid JSON data", status=400)

        # Extract the selected cards (in the 'deck' category)
        
        leader = []
        base = []
        deck = []
        selected_cards_data = data['deck']
        for card in selected_cards_data:
            if card['card_type'] =='Leader': leader.append({"id": card["id"], "count": card["count"]})
            elif card['card_type'] =='Base': base.append({"id": card["id"], "count": card["count"]})
            else: deck.append({"id": card["id"], "count": card["count"]})
        swudb_deck_data = {}
        swudb_deck_data['metadata'] = {"name":"Sealed Format Deck","author":"SWU-Boosters.onrender.com"}
        swudb_deck_data['leader'] = leader[0]
        swudb_deck_data['secondleader'] = leader[1] if len(leader) > 1 and leader[1] is not None else None
        swudb_deck_data['base'] = base[0]
        swudb_deck_data['deck'] = deck

        # Return the selected cards as a downloadable JSON file
        response = Response(json.dumps(swudb_deck_data, indent=4), mimetype='application/json')
        response.headers["Content-Disposition"] = "attachment; filename=selected_cards.json"
        return response

    except Exception as e:
        # Handle any unexpected errors
        print(f"Error processing JSON data: {e}")
        return Response("Error processing JSON data", status=500)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)