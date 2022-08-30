from pywebio.input import input, FLOAT, input_group, NUMBER, PASSWORD, select, checkbox
from pywebio.output import put_text, put_row, put_code, put_buttons, clear, popup, remove, put_scope, put_image, toast, \
    put_column, put_table
from pywebio import start_server, config
from pywebio.session import run_js
from pywebio_battery import get_cookie, set_cookie
import os
import mod

logged = False

roles = ['heroine', 'rival', 'partner', 'exmidboss', 'onetruepartner', 'stageboss', 'finalboss', 'challenger', 'antiheroine',
         'exboss', 'mobboss', 'secretboss', 'lonewolf', 'phantasmboss', 'backstage']

pictures = {'default': 'http://remiliowo.ddns.net/default.jpg'}

def btn_clk(typ):
    global gamers
    if typ == 'Login':
        clear()
        cope()
        loginf()
    elif typ == 'Register':
        clear()
        cope()
        register()
    elif typ == 'Stats':
        clear()
        menu()
    elif typ == 'Newgame':
        clear()
        newgame()
    elif typ == 'add':
        adduser()
    elif typ == 'finish':
        print(gamers)
        mod.end_game(gamers)
        clear()
        panel()

@config(theme="dark")
def cope():
    global cuser
    login = get_cookie('login')
    passwd = get_cookie('passwd')

    if login != None and passwd != None:
        u = mod.load(login)
        cuser = u
        panel()
    else:
        loginf()



def register():
    info = input_group("Rejestracja", [
        input('Podaj Nick', name='name', required=True),
        input('Podaj Haslo', name='pswd', required=True, type=PASSWORD)
    ], cancelable=True)
    try:
        u = mod.User(info['name'], info['pswd'])

        if mod.save(u):
            popup('Nick w uzyciu!')
        else:
            clear()
            panel()
    except: pass

def loginf():
    global cuser
    info = input_group("Logowanie", [
        input('Podaj Nick', name='name', required=True),
        input('Podaj Haslo', name='pswd', required=True, type=PASSWORD)
    ])
    u = mod.load(info['name'])
    if u == True:
        popup('Nie ma takiego nicku')
        loginf()
    else:
        if u.passwd != info['pswd']:
            popup('Zle haslo!')
            loginf()
        else:
            set_cookie('login', info['name'])
            set_cookie('passwd', info['pswd'])
            run_js('window.location.reload()')
            cuser = u



    clear()


def panel(suser = None):
    clear()
    global cuser
    if suser is None:
        suser = cuser
    s = []
    twins = len(suser.wins)
    lose = len(suser.loses)
    for r in roles:
        c = 0
        v = 0
        for w in suser.wins:
            if r == w:
                c += 1
        for l in suser.loses:
            if r == l:
                v += 1
        try:
            wynik = round((c / (c + v)) * 100, 2)
        except:
            wynik = 0

        s.append(f'{c}W {v}L WR:{wynik}%\n')



    put_text(f'Zalogowano jako {cuser.nick}')

    if cuser.admin:
        put_buttons(['Register', 'Newgame'], onclick=btn_clk)
    put_buttons(['Stats'], onclick=btn_clk)

    put_text(f'{suser.nick}').style(f'font-size: 50px; font-family: "Comic Sans MS", "Chalkboard SE", "Comic Neue", sans-serif;')
    put_row([
        put_image(pictures[suser.pfp], width=f'200px', height=f'200px').onclick(lambda: toast('You click the image')),

        put_column([
            put_text(f'Wygrane: {twins}'),
            put_text(f'Przegrane: {lose}'),
            put_text(f'Śmierdzi: {suser.deaths}'),
            put_text(f'Gier Totalnie: {twins+lose}'),
            put_text(f'W/R: {round((twins/1)*100, 2)}%')
        ]).style(f'font-size: 25px; font-family: "Comic Sans MS", "Chalkboard SE", "Comic Neue", sans-serif; line-height: 0.8'),

        put_text(f'Congratulation no badge given')
    ])
    put_row([
        put_table([['heroine', 'rival', 'partner', 'exmidboss', 'onetruepartner', 'stageboss', 'finalboss', 'challenger', 'antiheroine',
            'exboss', 'mobboss', 'secretboss', 'lonewolf', 'phantasmboss', 'backstage'],
            s])
    ]).style(f'padding-top: 35px;')


def menu():
    userki = []

    users = os.listdir('users')

    for x in users:
        userki.append(mod.load(x.split('.')[0]))
    userki.sort(key=lambda y: len(y.wins), reverse=True)

    for h in range(0,len(userki)):
        x = userki[h]
        put_row([

            put_image(pictures[x.pfp], width='50px', height='50px'),
            put_text(f'{x.nick}').onclick(lambda x=x: panel(x)),
            put_text(len(x.wins))

        ]).style(f'font-size: 40px; font-family: "Comic Sans MS", "Chalkboard SE", "Comic Neue", sans-serif; line-height: 0.8')

def newgame():
    global gamers
    global holder
    holder = []
    gamers = []
    put_buttons(['add', 'finish'], onclick=btn_clk)


def adduser():
    global gamers
    userki = []

    users = os.listdir('users')

    for x in users:
        userki.append((x.split('.')[0]))

    info = input_group('Add user', [
        select('Podaj Nick', userki, name='name', required=True),
        select('Podaj Role', roles, name='role', required=True),
        checkbox('Zaznacz', options=['Wygral', 'Przezyl'], name='check'),
    ], cancelable=True)
    x = (mod.load(info['name']))
    gamers.append(info)
    s = f'Status: '
    if 'Wygral' in info['check']:
        s+=f'W'
    if 'Przezyl' in info['check']:
        s+= f'P'

    put_row([

        put_image(pictures[x.pfp], width='50px', height='50px'),
        put_text(f'{x.nick}'),
        put_text(f'{info["role"]}'),
        put_text(s)

    ]).style(f'font-size: 40px; font-family: "Comic Sans MS", "Chalkboard SE", "Comic Neue", sans-serif; line-height: 0.8')

if __name__ == '__main__':

    start_server(cope, port=80, debug=True)



