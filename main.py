from flask import Flask, render_template, request, Response
import csv
import json
import random
import copy
from flask_mail import Mail, Message
import string
import os
from dotenv import load_dotenv
from threading import Thread


load_dotenv()


app = Flask(__name__, template_folder='templates')


deck_code = ''

# Configure Flask-Mail
app.config.update(
    MAIL_SERVER='smtp.gmail.com',        # Replace with your email provider's SMTP server
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='swuboosters@gmail.com', # Replace with your email
    MAIL_PASSWORD= os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER='swuboosters@gmail.com'  # Default "from" email
)
mail = Mail(app)


# Load the card collection from CSV
collection = []
with open('SWU_all_cards.csv', 'r', encoding='ISO-8859-1') as file:
    Reader = csv.reader(file)
    for line in Reader:
        collection.append(line)
showcase_collection = []
with open('SWU_showcase.csv', 'r', encoding='ISO-8859-1') as file:
    Reader = csv.reader(file)
    for line in Reader:
        showcase_collection.append(line)
hyperspace_collection = []
with open('SWU_hyperspace.csv', 'r', encoding='ISO-8859-1') as file:
    Reader = csv.reader(file)
    for line in Reader:
        hyperspace_collection.append(line)

full_card_pool = []
full_showcase_pool = []
full_hyperspace_pool = []

# Ensure each card appears in the pool according to its count in the collection
for c in collection[1:]:
    count = int(c[4])
    card = c[:4] + c[5:]
    for i in range(count):
        full_card_pool.append(card)

for c in showcase_collection[1:]:
    count = int(c[4])
    card = c[:4] + c[5:]
    for i in range(count):
        full_showcase_pool.append(card)

for c in hyperspace_collection[1:]:
    count = int(c[4])
    card = c[:4] + c[5:]
    for i in range(count):
        full_hyperspace_pool.append(card)



# This creates one booster pack according to the distribution rules
def get_booster(set='sor',qty = "1",):

    card_pool = {}
    showcase_pool = {}
    hyperspace_pool = {}
    packs = []
    
    index = 0
    for c in full_card_pool:
        if  c[0] == set:
            card_pool[index] = c
            index += 1

    index = 0

    for c in full_showcase_pool:
        if  c[0] == set:
            showcase_pool[index] = c
            index += 1


    index = 0
    for c in full_hyperspace_pool:
        if  c[0] == set:
            hyperspace_pool[index] = c
            index += 1

    hyperspace_leader_pool = {}
    index = 0
    for c in full_hyperspace_pool:
        if  c[0] == set and c[4] == "Leader":
            hyperspace_leader_pool[index] = c
            index += 1

    hyperspace_base_pool = {}
    index = 0
    for c in full_hyperspace_pool:
        if  c[0] == set and c[4] == "Base":
            hyperspace_base_pool[index] = c
            index += 1



    rare_leaders = {}
    leaders = {}
    bases = {}
    commons = {}
    uncommons = {}
    rares = {}
    legendaries = {}

    for i in range(int(qty)):

        hyperspace_number = random.randint(1, 100)
        hyper = "None"
        if hyperspace_number <= 2: hyper = "Legendary"
        elif hyperspace_number <= 9: hyper = "Rare"
        elif hyperspace_number <= 22: hyper = "Uncommon"
        elif hyperspace_number <= 62: hyper = "Common"

        hyperspace_leader_number = random.randint(1, 20)
        hyper_leader = False
        if hyperspace_leader_number == 1: hyper_leader = True

        hyperspace_base_number = random.randint(1, 20)
        hyper_base = False
        if hyperspace_base_number == 1: hyper_base = True

        hyperspace_foil_number = random.randint(1, 20)
        hyper_foil = False
        if hyperspace_foil_number == 1: hyper_foil = True

        showcase_number = random.randint(1, 288)
        showcase_leader = False
        if showcase_number <=10: showcase_leader = True

        pack = []
        for k, v in card_pool.items():
            if v[4] == 'Leader' and v[17] in ['Rare','Special']: rare_leaders[k] = v
            elif v[4] == 'Leader': leaders[k] = v
            elif v[4] == 'Base' and v[17] != 'Rare' : bases[k] = v
            elif v[17] == 'Common': commons[k] = v
            elif v[17] == 'Uncommon': uncommons[k] = v
            elif v[17] in ['Rare','Special']: rares[k] = v
            elif v[17] == 'Legendary': legendaries[k] = v

        # 1 Leader, 1 Base, 9 Commons, 3 Uncommons, 1 Rare/Legendary, 1 random card
        random_number = random.randint(1, 6)
        if random_number == 6: leader_index = random.choice(list(rare_leaders.keys()))
        else: leader_index = random.choice(list(leaders.keys()))
        leader = copy.deepcopy(card_pool[leader_index])
        if showcase_leader and len(showcase_pool) >0: 
            leader_index = random.choice(list(showcase_pool.keys()))
            leader = copy.deepcopy(showcase_pool[leader_index])
        elif hyper_leader and len(hyperspace_leader_pool) > 0:
            leader_index = random.choice(list(hyperspace_leader_pool.keys()))
            leader = copy.deepcopy(hyperspace_leader_pool[leader_index])

        leader.append('1 Leader')
        pack.append(leader)


        base_index = random.choice(list(bases.keys()))
        base = copy.deepcopy(card_pool[base_index])
        if hyper_base and len(hyperspace_base_pool) > 0:
            base_index = random.choice(list(hyperspace_base_pool.keys()))
            base = copy.deepcopy(hyperspace_base_pool[base_index])
            while base[-3] == "Rare":
                base_index = random.choice(list(hyperspace_base_pool.keys()))
                base = copy.deepcopy(hyperspace_base_pool[base_index]) 

        base.append('1 Base')
        pack.append(base)
        
        common_indeces = []
        for i in range(9):
            common_index = random.choice(list(commons.keys()))
            while common_index in common_indeces:
                common_index = random.choice(list(commons.keys()))
            common_indeces.append(common_index)

            common = copy.deepcopy(card_pool[common_index])
            if hyper == "Common" and i == 0:
                card_number = common[-1]
                card_name = common[2]
                for k,v in hyperspace_pool.items():
                    if v[-1] == card_number and v[2] == card_name:
                        common = copy.deepcopy(v)
            common.append(f"{i+1} of 9 Commons")
            pack.append(common)
        
        uncommon_indeces = []
        for i in range(3):
            uncommon_index = random.choice(list(uncommons.keys()))
            while uncommon_index in uncommon_indeces:
                uncommon_index = random.choice(list(uncommons.keys()))
            uncommon_indeces.append(uncommon_index)
            
            uncommon = copy.deepcopy(card_pool[uncommon_index])

            if hyper == "Uncommon" and i == 0:
                card_number = uncommon[-1]
                card_name = uncommon[2]
                print(uncommon[2])
                for k,v in hyperspace_pool.items():
                    if v[-1] == card_number and v[2] == card_name:
                        uncommon = copy.deepcopy(v)
                print(uncommon[2])

            if (hyper == "Rare" or hyper == "Legendary") and i == 2:
                random_number = random.randint(1, 8)
                if len(legendaries) > 0 and hyper == "Legendary":
                    rare_index = random.choice(list(legendaries.keys()))
                else:
                    rare_index = random.choice(list(rares.keys()))
                rare = copy.deepcopy(card_pool[rare_index])
                card_number = rare[-1]
                card_name = rare[2]
                for k,v in hyperspace_pool.items():
                    if v[-1] == card_number and v[2] == card_name:
                        uncommon = copy.deepcopy(v)

            uncommon.append(f"{i+1} of 3 Uncommons")
            pack.append(uncommon)

        random_number = random.randint(1, 8)
        if len(legendaries) > 0 and random_number == 8:
            rare_index = random.choice(list(legendaries.keys()))
        else:
            rare_index = random.choice(list(rares.keys()))
        rare = copy.deepcopy(card_pool[rare_index])

        # RARE AND LEGENDARY HYPERSPACE SHOULD BE IN UNCOMMONS, NOT HERE
        # if hyper == "Rare" or hyper == "Legendary":
        #     card_number = rare[-1]
        #     card_name = rare[2]
        #     for k,v in hyperspace_pool.items():
        #         if v[-1] == card_number and v[2] == card_name:
        #             rare = copy.deepcopy(v)

        rare.append("1 Rare or Legendary")
        pack.append(rare)

        any_card_index = random.choice(list(card_pool.keys()))
        any_card_type = card_pool[any_card_index][4]
        while any_card_type == 'Leader' or any_card_type == 'Base':
            any_card_index = random.choice(list(card_pool.keys()))
            any_card_type = card_pool[any_card_index][4]
        any_card = copy.deepcopy(card_pool[any_card_index])  

        if hyper_foil:
            any_card_index = random.choice(list(hyperspace_pool.keys()))
            any_card_type = hyperspace_pool[any_card_index][4]
            while any_card_type == 'Leader' or any_card_type == 'Base':
                any_card_index = random.choice(list(hyperspace_pool.keys()))
                any_card_type = hyperspace_pool[any_card_index][4]
            any_card = copy.deepcopy(hyperspace_pool[any_card_index]) 


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

def send_email_async(app,msg):
    with app.app_context():
        mail.send(msg)


@app.route('/generate_json', methods=['POST'])
def generate_json():
    try:
        # Get the selected cards from the request JSON
        data = request.get_json()
        
        # Check if the data is valid
        if not data or 'deck' not in data:
            return Response("Invalid JSON data", status=400)

        # Extract the selected cards (in the 'deck' category)
        deck_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

        leader = []
        base = []
        deck = []
        selected_cards_data = data['deck']
        for card in selected_cards_data:
            if card['card_type'] =='Leader': leader.append({"id": card["id"], "count": card["count"]})
            elif card['card_type'] =='Base': base.append({"id": card["id"], "count": card["count"]})
            else: deck.append({"id": card["id"], "count": card["count"]})
        swudb_deck_data = {}
        swudb_deck_data['metadata'] = {"name":f"Booster Deck {deck_code}","author":"SWU-Boosters.onrender.com"}
        swudb_deck_data['leader'] = leader[0]
        swudb_deck_data['secondleader'] = leader[1] if len(leader) > 1 and leader[1] is not None else None
        swudb_deck_data['base'] = base[0]
        swudb_deck_data['deck'] = deck

        # Return the selected cards as a downloadable JSON file
        response = Response(json.dumps(swudb_deck_data, indent=4), mimetype='application/json')
        response.headers["Content-Disposition"] = "attachment; filename=selected_cards.json"

        # Email the JSON file
        msg = Message(f"DECK {deck_code}", recipients=["swuboosters@gmail.com"])
        msg.body = f"Here is the json for deck {deck_code}."
        # Attach the JSON data as a file
        msg.attach(f"deck_{deck_code}.json", "application/json", json.dumps(swudb_deck_data, indent=4))
        
        # Send the email
        Thread(target=send_email_async, args=(app, msg)).start()

        
        
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