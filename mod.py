import pickle
import os

fold = f'users/'

users = os.listdir('users')


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

        self.wins = []
        self.loses = []
        self.deaths = 0
        self.plays = 0
        self.rp = 0

def end_game(info):
    for x in info:

        u = load(x['name'])
        u.plays += 1
        if 'Wygral' in x['check']:
            u.wins.append(x['role'])
        else:
            u.loses.append(x['role'])
        if 'Przezyl' not in x['check']:
            u.deaths += 1

        save(u)


