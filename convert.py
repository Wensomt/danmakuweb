import os
import mod

fold = f'users/'

users = os.listdir('users')

for x in users:
    u = mod.load(x.split('.')[0])
    #u.title = 'Wruszka'
    #u.titles = ['Wruszka']
    u.wordly_won = 0
    u.wordly_max_streak = 0
    u.wordly_cur_streak = 0
    u.wordly_win = False
    u.wordly_win_today = False
    u.wordly_tries = []
    mod.save(u)