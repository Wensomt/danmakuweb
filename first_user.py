import os
import mod

def first():
    u = mod.User("Wensomt","Gengetsu")
    mod.save(u)

def adminset(user):
    u = mod.load(user)
    u.admin = True
    mod.save(u)

adminset("Wensomt")