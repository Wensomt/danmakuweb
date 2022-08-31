import pickle
import os

fold = f'users/'

users = os.listdir('users')

def load_pics():
    al = os.listdir('pictures')
    o = {}
    for x in al:
        with open(f'pictures/{x}', 'rb') as f:
            obr = f.read()
        o[x.split('.')[0]] = obr

    return o

def save(user):
    with open(f'{fold}{user.nick}.user', 'wb') as f:
        pickle.dump(user, f)
        return False

def load(uid):
        with open(f'{fold}{uid}.user', 'rb') as f:
            user = pickle.load(f)
        return user


class User:
    def __init__(self, nick, passwd):
        self.nick = nick
        self.passwd = passwd
        self.admin = False
        self.pfp = f'default'
        self.badges = ['default']
        self.badge = 'default'
        self.avatar = ['default']
        self.history = []
        self.rc = 0
        self.huj = {}


def end_game(info):

    ig = len(info)
    print(info)
    for x in info:
        r = 0
        u = load(x['name'])
        u.history.append(x)

        if 'Przezyl' in x['check'] and 'Wygral' in x['check']:
            r += 100
        elif 'Wygral' in x['check']:
            r += 50
        elif 'Przezyl' in x['check']:
            r += 50
        else:
            r += 25

        match x['role']:
            case 'Heroine':
                r += 50
            case 'Rival':
                r += 50
            case 'Partner':
                r += 0
            case 'EX Midboss':
                r += 25
            case 'One True Partner':
                r += 75
            case 'Stage Boss':
                r += 0
            case 'Final Boss':
                r += 25
            case 'Challenger':
                r += 50
            case 'Anti-Heroine':
                r += 50
            case _:
                r += 50

        match ig:
            case 5:
                r = round(r*1.1)
            case 6:
                r = round(r*1.3)
            case 7:
                r = round(r*1.6)
            case 8:
                r = round(r*2)

        u.rc = r
        save(u)


