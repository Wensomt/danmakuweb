import pickle
import os

fold = f'users/'

users = os.listdir('users')


def save(user):
    if f'{user.nick}.user' not in users:
        with open(f'{fold}{user.nick}.user', 'wb') as f:
            pickle.dump(user, f)
        return False
    else:
        return True

def load(uid):
    try:
        with open(f'{fold}{uid}.user', 'rb') as f:
            user = pickle.load(f)
        return user
    except: return True


class User:
    def __init__(self, nick, passwd):
        self.nick = nick
        self.passwd = passwd