import os
import mod

fold = f'users/'

users = os.listdir('users')

for x in users:
    u = mod.load(x.split('.')[0])
    u.title = 'Wruszka'
    u.titles = ['Wruszka']
    mod.save(u)