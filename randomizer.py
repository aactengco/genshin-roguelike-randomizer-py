from concurrent.futures import process
import csv
from random import randint

# Constants #
INT_FIELDS = ['own', 'rarity', 'weight']



# Functions #
def getEffectiveWeight(character: dict):
    return character['weight'] * character['own'] * character['available']

def getSumWeight(characters: dict):
    sum_weight = sum([getEffectiveWeight(character) for character in characters.values()])
    return sum_weight

def getRandomChar(characters: dict, weight: int = -1):
    weight = weight if weight >= 0 \
        else randint(0, getSumWeight(characters))
    for character in characters.values():
        weight -= getEffectiveWeight(character)
        if weight <= 0:
            return character['name']
    print('ERROR in getRandomChar: no character found')
    exit(-1)

def pullChars(num_pulls: int, characters: dict):
    pulls = []
    while len(pulls) < min(num_pulls, len(characters)):
        sum_weight = getSumWeight(characters)
        if sum_weight == 0:
            print('ERROR in pullChars: SUM WEIGHT IS ZERO')
            exit(-1)
        character_name = getRandomChar(characters)
        characters[character_name]['available'] = 0
        pulls.append(character_name)
    return pulls

def processInput(user_input: str, characters: dict, picked_characters: list):
    user_input = user_input.lower()
    if (user_input in ['c', 'chars', 'characters']):
        print('SELECTED CHARACTERS:')
        for character_name in picked_characters:
            print(character_name)
        print()
    if (user_input in ['a', 'available']):
        print('AVAILABLE CHARACTERS')
        for character in characters.values():
            if (character['own'] * character['available']):
                print(character['name'])
        print()



characters = {}

# Import Data #
with open('characters.csv', 'r') as characters_data_raw:
    characters_data = list(csv.reader(characters_data_raw))
    headers = characters_data[0]
    for i in range(1, len(characters_data)):
        character_data = characters_data[i]
        character = {headers[i]: character_data[i] for i in range(len(headers))}
        character['available'] = 1
        for field in INT_FIELDS:
            character[field] = int(character[field])
        characters[character['name']] = character



# Main #
target = 10
num_options = 3
characters_picked = []
for i in range(target):
    user_input = -1
    pick_options = pullChars(num_options, characters)
    while(user_input < 0 or user_input >= num_options):
        print(f'# PICK {i+1} #')
        for j in range(len(pick_options)):
            print(f'[{j}] {pick_options[j]}')
        user_input = input('Select Character: ')
        print()
        print()
        print()
        processInput(user_input, characters, characters_picked)
        user_input = int(user_input) if user_input.isdigit() else -1
    pick = pick_options[user_input]
    characters_picked.append(pick)
    print(f'{pick} selected')
    print()
print()
print()
print()
print('CHARACTERS SELECTED')
print('-------------------')
print()
for pick in characters_picked:
    print(pick)