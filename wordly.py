import pickle
import os
import random

wordly_dir = f'wordly_data/'

def get_characters():
    with open(f'{wordly_dir}characters.wordly', 'rb') as f:
        characters = pickle.load(f)
    return characters

def get_today_character():
    with open(f'{wordly_dir}today_character.wordly', 'rb') as f:
        character = pickle.load(f)
    return character

def load_pictures():
    al = os.listdir('wordly_data/pictures')
    o = {}
    for x in al:
        with open(f'wordly_data/pictures/{x}', 'rb') as f:
            obr = f.read()
        o[x.split('.')[0]] = obr

    return o

class Character:
    def __init__(self, name, race, home, first, head, hair, atrb):
        self.name = name
        self.race = race
        self.home = home
        self.first = first
        self.head = head
        self.hair = hair
        self.atrb = atrb

def new_wordly():
    characters = get_characters()
    character = characters[random.randint(0, len(characters))]
    print(character.name[0])
    with open(f'{wordly_dir}today_character.wordly', 'wb') as f:
        pickle.dump(character, f)

