import pickle
import os

fold = f'users/'
data_file = f'data/'

users = os.listdir('users')



def load_badge():
    al = os.listdir('badges')
    o = {}
    for x in al:
        with open(f'badges/{x}', 'rb') as f:
            obr = f.read()
        o[x.split('.')[0]] = obr

    return o

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
        self.title = 'Wruszka'
        self.titles = ['Wruszka']
        self.huj = {}
        self.won = 0
        self.max_streak = 0
        self.cur_streak = 0


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

        if x['role'] == 'Heroine':
            r += 50
        elif x['role'] == 'Rival':
            r += 50
        elif x['role'] == 'Partner':
            r += 0
        elif x['role'] == 'EX Midboss':
            r += 25
        elif x['role'] == 'One True Partner':
            r += 75
        elif x['role'] == 'Stage Boss':
            r += 0
        elif x['role'] == 'Final Boss':
            r += 25
        elif x['role'] == 'Challenger':
            r += 50
        elif x['role'] == 'Anti-Heroine':
            r += 50
        else:
            r += 25


        if ig == 5:
            r = round(r*1.1)
        if ig == 6:
            r = round(r*1.3)
        if ig == 7:
            r = round(r*1.6)
        if ig == 8:
            r = round(r*2)

        cirno = 0
        for y in u.history:
            if y['postac'] == 'Cirno':
                cirno += 1
            if y['role'] =='Anti-Heroine':
                cirno += 1
        if cirno == 9:
            if 'Baka' not in u.badges:
                u.badges.append('Baka')
                u.titles.append('The Baka')
                r += 400

        u.rc += r
        save(u)

def read_data(data):
    with open(f'{data_file}{data}.txt', 'r') as f:
        data_list = f.readline().split(', ')
        return [x.replace('\'', '') for x in data_list]

def add_data(data,to_add):
    with open(f'{data_file}{data}.txt', 'a') as f:
        f.write(", '"+to_add+"'")
