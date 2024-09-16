import os
import mod
import pickle
import wordly
def first():
    u = mod.User("Wensomt","Gengetsu")
    mod.save(u)

def adminset(user):
    u = mod.load(user)
    u.admin = True
    mod.save(u)

def create_characters_data():
    data = []
    with open(f'genso.csv','r', encoding='utf-8') as f:
        #clean = f.read().replace('\n', '')
        for line in f:
            y = line.split(',')
            char_tab = []
            for x in y:
                char_tab.append(x.split(';'))
            max = len(char_tab)
            max_max = len(char_tab[max-1])
            char_tab[max-1][max_max-1] = char_tab[max-1][max_max-1][:-1]

            char = wordly.Character(char_tab[0],char_tab[1],char_tab[2],char_tab[3],char_tab[4],char_tab[5],char_tab[6])
            data.append(char)
    with open(f'wordly_data/characters.wordly', 'wb') as f:
        pickle.dump(data, f)
        return False

create_characters_data()
#adminset("Wensomt")