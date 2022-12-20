import os
import mod

fold = f'users/'

users = os.listdir('users')

for x in users:
    u = mod.load(x.split('.')[0])
    #u.title = 'Wruszka'
    #u.titles = ['Wruszka']
    u.won = 0
    u.max_streak = 0
    u.cur_streak = 0
    mod.save(u)