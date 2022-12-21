import pywebio
import pywebio_battery
from pywebio.input import input, FLOAT, input_group, NUMBER, PASSWORD, select, checkbox
from pywebio.output import put_text, put_row, put_code, put_buttons, clear, popup, remove, put_scope, put_image, toast, \
    put_column, put_table, put_grid, close_popup, use_scope, put_button
from pywebio import start_server, config
from pywebio.session import run_js
from pywebio_battery import get_cookie, set_cookie
import os
import mod
import time
import threading
import pickle
import schedule
import wordly

def read_roles():
    return mod.read_data("roles")


def read_postacie():
    return mod.read_data("postacie")


pictures = mod.load_pics()
prices = {'Alice': 300, 'Chen': 300, 'Chen2': 300, 'Cirno': 300, 'Cirno2': 300, 'Cirnuch': 300, 'Clownpiece': 300,
          'default': 0, 'Flan': 300, 'Flandre': 300, 'Kappa': 300, 'Koakuma': 300, 'Kogasa': 300, 'Koishi': 300,
          'Koishi2': 300, 'Koishi3': 300, 'Kokoro': 300, 'Marisa': 300, 'Marisa2': 300, 'Marisa3': 300, 'Miko': 300,
          'Miko2': 300, 'Misumaru': 300, 'Mokou': 300, 'Mokou1': 300, 'Momiji': 300, 'Okuu': 300, 'Patchouli': 300,
          'Patchouli2': 300, 'Reimu': 300, 'Reimu2': 300, 'Reimu3': 300, 'Reisen': 300, 'Reisen2': 300, 'Remi': 300,
          'Remilia': 300, 'Remilia2': 300, 'Remilia3': 300, 'Remilia4': 300, 'Renko': 300, 'Rumia': 300, 'Rumia2': 300,
          'Sakuya': 300, 'Sanae': 300, 'Sanae2': 300, 'Satori': 300, 'Seiga': 300, 'Seiga2': 300, 'Seiga3': 300,
          'Suika': 300, 'Suika2': 300, 'Suwako': 300, 'Youmuu': 300, 'Yukari': 300, 'Yukari2': 300, 'Yukari3': 300,
          'Yukari4': 300, 'Yuugi': 300, 'Yuuka': 300, 'Yuyuko2': 300, 'Yuyuko3': 300, 'Yuyuko4': 300, 'Yuyuko5': 300,
          'gamer': 700, 'fumoo': 700, 'tomasz': 800, 'troll': 1000, 'remiliacry': 3000, 'boomer': 1000,
          'suwapepe': 1200}

badges = mod.load_badge()
badge_desp = {'Are you watching Change': 'Dobierz 5 kart o wartości 1 punkta za pomocą spellcardu Junko',
              'Arrest him': 'Odrzuć 7 kart poprzez efekt karty innego gracza',
              'Baka': 'zagraj 9 gier jako cirno lub antiheroine (sumuje sie)',
              'Cope': 'Uniknij 5 ataków w jednej turze',
              'Cunny': 'Każdy z graczy gra loli postacią w grze z 6/7/8 graczy', 'default': 'Witaj nowy!',
              'Dig it Dig Out': 'Podczas twojej tury z efektu jednej karty odkryjesz lub dobierzesz conajmniej 10 kart',
              'Emotional Damage': 'Zadaj jednym atakiem 4 obrażenia',
              'Four of a Kind': 'Posiadaj 3 extra postacie naraz', 'Neko': 'Zagraj 7 gier jako chen lub rin',
              'Skill Isue': 'Wygraj jako ostani żywy gracz w grze z 7/8 graczami',
              'Spin': 'Grając jako Hina spowoduj, żeby inny gracz podczas swojego draw stepu dobrał 6 kart',
              'Spring Has Arrived': 'Zgin poprzez strate żyj na skutek incydentu "Lily White"',
              'Tank Marisa': 'Posiadaj 4 karty Power Up jako Marisa',
              'There is no escape': 'Podczas twojego main stepu inny gracz ginie nie na wskutek ataku'}

avtitles = {'default': 'Wruszka', 'Baka': 'The Baka', 'Are you watching Change': 'Patrz Change To',
            'Arrest him': 'Aresztowany', 'Cope': 'Kołper', 'Cunny': 'Lolipilled', 'Dig it Dig Out': 'I love minecraft',
            'Emotional Damage': 'Emotionally Unstable', 'Four of a Kind': 'Kserokopia', 'Neko': 'Neko-Chan',
            'Skill Isue': 'Skilled', 'Spring Has Arrived': 'Powiew Wiosny', 'Tank Marisa': 'Chad',
            'Spin': 'Sok Fortuna', 'There is no escape': 'Bez możliwości ucieczki'}

wordly_pictures = wordly.load_pictures()

def checklogin(u):
    l = get_cookie('login')
    p = get_cookie('passwd')
    if u.nick == l and u.passwd == p:
        return True
    else:
        return False


def btn_clk(typ):
    global gamers
    global data_add
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
        mod.end_game(gamers)
        clear()
        panel()
    elif typ == 'Store':
        clear()
        store()
    elif typ == 'Back':
        clear()
        panel()
    elif typ == 'AddBadge':
        clear()
        addbadge()
    elif typ == 'AddRMC':
        addRMC()
    elif typ == 'BadgeList':
        clear()
        showbadges()
    elif typ == 'Description':
        despedit()
    elif typ == 'Title':
        title()
    elif typ == 'Dodaj Role':
        add_role()
    elif typ == 'Dodaj Postac':
        add_postac()
    elif typ == 'Wordly':
        wordly_panel()


@config(theme="dark")
def cope():
    login = get_cookie('login')
    passwd = get_cookie('passwd')

    if login != None and passwd != None:
        u = mod.load(login)
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
    except:
        pass


def loginf():
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
            cuser = u
            set_cookie('login', info['name'])
            set_cookie('passwd', info['pswd'])

            run_js('window.location.reload()')

    clear()


def panel(suser=None):
    clear()
    cuser = mod.load(get_cookie('login'))
    if not checklogin(cuser):
        return

    if suser is None:
        suser = cuser
    rw = []
    rl = []
    s = []
    hist = suser.history
    twins = 0
    lose = 0
    deaths = 0
    hist.reverse()
    for h in hist:
        if 'Wygral' in h['check']:
            twins += 1
            rw.append(h['role'])
        else:
            lose += 1
            rl.append(h['role'])
        if 'Przezyl' in h['check']:
            pass
        else:
            deaths += 1

    roles = read_roles()
    for r in roles:
        c = 0
        v = 0
        for w in rw:
            if r == w:
                c += 1
        for l in rl:
            if r == l:
                v += 1
        try:
            wynik = round((c / (c + v)) * 100, 2)
        except:
            wynik = 0

        s.append(f'{c}W {v}L WR:{wynik}%\n')

    if lose + twins == 0:
        sumka = 1
    else:
        sumka = lose + twins
    wr = round((twins / sumka) * 100, 2)

    put_text(f'Zalogowano jako {cuser.nick}')

    put_buttons(['Wordly'],onclick=btn_clk)
    if cuser.admin:
        put_buttons(['Register', 'Newgame', 'AddBadge', 'AddRMC', 'Dodaj Role', 'Dodaj Postac'], onclick=btn_clk)
    put_row([
        put_buttons(['Stats', 'Store', 'BadgeList', 'Description', 'Title', 'Back'], onclick=btn_clk),
        put_text(f"RemiCoins: {cuser.rc}").style(
            f'font-size: 25px; font-family: "Comic Sans MS", "Chalkboard SE", "Comic Neue", sans-serif; color: red')
    ])

    put_row([put_text(f'{suser.title} {suser.nick}').style(
        f'font-size: 50px; font-family: "Comic Sans MS", "Chalkboard SE", "Comic Neue", sans-serif;')
             ])

    put_row([
        put_image(pictures[suser.pfp], width=f'200px', height=f'200px').onclick(lambda: choose_avatar(suser)),

        put_column([
            put_text(f'Wygrane: {twins}'),
            put_text(f'Przegrane: {lose}'),
            put_text(f'Śmierdzi: {deaths}'),
            put_text(f'Gier Totalnie: {twins + lose}'),
            put_text(f'W/R: {wr}%')
        ]).style(
            f'font-size: 25px; font-family: "Comic Sans MS", "Chalkboard SE", "Comic Neue", sans-serif; line-height: 0.8'),

        put_image(badges[suser.badge], width=f'200px', height=f'200px').onclick(lambda: choose_badge(suser))
    ])
    try:
        dupa = suser.huj['desp']
    except:
        dupa = f'Brak opisu'
    put_text(dupa)
    roles = read_roles()
    put_text(f'Badges:').style(
        f'font-size: 35px; font-family: "Comic Sans MS", "Chalkboard SE", "Comic Neue", sans-serif; line-height: 0.8;padding-top: 35px;')
    put_grid(badgen(suser), cell_width='65px', cell_height='65px').style(f'padding-top: 35px;')
    put_row([
        put_table([roles, s]).style(f'width: 100%;')
    ]).style(f'padding-top: 35px;')

    put_row([
        put_text(f'HISTORIA GIER').style(
            f'font-size: 35px; font-family: "Comic Sans MS", "Chalkboard SE", "Comic Neue", sans-serif; line-height: 0.8')
    ])

    n = [["Postac", 'Rola', 'Win/Loss', 'Przezyl?']]
    for h in suser.history:
        m = []
        m.append(h['postac'])
        m.append(h['role'])
        if 'Wygral' in h['check']:
            m.append('Wygrana')
        else:
            m.append(f'Przegrana')
        if 'Przezyl' in h['check']:
            m.append(f'Przezyl')
        else:
            m.append(f'Smierc')
        n.append(m)
    put_row([
        put_table(n).style(f'width: 100%;')

    ]).style(
        f'font-size: 20px; font-family: "Comic Sans MS", "Chalkboard SE", "Comic Neue", sans-serif; line-height: 3')


def menu():
    userki = []

    users = os.listdir('users')

    for x in users:
        userki.append(mod.load(x.split('.')[0]))

    for x in userki:
        hist = x.history
        x.twins = 0
        for h in hist:
            if 'Wygral' in h['check']:
                x.twins += 1

    userki.sort(key=lambda y: y.twins, reverse=True)

    for h in range(0, len(userki)):
        x = userki[h]
        put_row([

            put_image(pictures[x.pfp], width='50px', height='50px'),
            put_text(f'{x.title}'),
            put_text(f'{x.nick}').onclick(lambda x=x: panel(x)),
            put_text(x.twins)

        ]).style(
            f'font-size: 40px; font-family: "Comic Sans MS", "Chalkboard SE", "Comic Neue", sans-serif; line-height: 0.8')


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
    roles = read_roles()
    postacie = read_postacie()
    info = input_group('Add user', [
        select('Podaj Nick', userki, name='name', required=True),
        select('Podaj Role', roles, name='role', required=True),
        select('Podaj Postac', postacie, name='postac', required=True),
        checkbox('Zaznacz', options=['Wygral', 'Przezyl'], name='check'),
    ], cancelable=True)
    x = (mod.load(info['name']))
    gamers.append(info)
    s = f'Status: '
    if 'Wygral' in info['check']:
        s += f'W'
    if 'Przezyl' in info['check']:
        s += f'P'

    put_row([

        put_image(pictures[x.pfp], width='50px', height='50px'),
        put_text(f'{x.nick}'),
        put_text(f'{info["role"]}'),
        put_text(s),
        put_text(f'{info["postac"]}')

    ]).style(
        f'font-size: 25px; font-family: "Comic Sans MS", "Chalkboard SE", "Comic Neue", sans-serif; line-height: 0.8')


def imggen():
    cuser = mod.load(get_cookie('login'))
    m = []
    n = []
    c = 0
    for x in cuser.avatar:
        c += 1
        n.append(put_image(pictures[x], width='64px', height='64px', title=x).onclick(lambda x=x: choosed(x)))
        if c == 7:
            m.append(n.copy())
            n = []
            c = 0

    m.append(n)
    return m


def imggen2():
    cuser = mod.load(get_cookie('login'))
    m = []
    n = []
    c = 0
    for x in pictures:
        if x not in cuser.avatar:
            c += 1
            n.append(put_image(pictures[x], width='64px', height='64px', title=x).onclick(lambda x=x: buy(x)))
            n.append(put_text(f'{x}\n {prices[x]}').style(f'text-align: center;'))
            if c == 7:
                m.append(n.copy())
                n = []
                c = 0

    m.append(n)
    return m


def badgen(suser=None):
    cuser = mod.load(get_cookie('login'))
    if suser is None:
        suser = cuser
    m = []
    n = []
    c = 0
    for x in badges:
        if x in suser.badges:
            y = badge_desp[x]
            c += 1
            n.append(put_image(badges[x], width='64px', height='64px', title=x).onclick(lambda y=y: popup(y)))
            n.append(put_text(f'{x}').style(f'text-align: center;'))
            if c == 7:
                m.append(n.copy())
                n = []
                c = 0

    m.append(n)
    return m


def badgen3():
    m = []
    n = []
    c = 0
    for x in badges:
        y = badge_desp[x]
        c += 1
        n.append(put_image(badges[x], width='64px', height='64px', title=x).onclick(lambda y=y: popup(y)))
        n.append(put_text(f'{x}').style(f'text-align: center;'))
        if c == 6:
            m.append(n.copy())
            n = []
            c = 0

    m.append(n)
    return m


def badgen2():
    cuser = mod.load(get_cookie('login'))
    m = []
    n = []
    c = 0
    for x in badges:
        if x in cuser.badges:
            c += 1
            n.append(put_image(badges[x], width='64px', height='64px', title=x).onclick(lambda x=x: chooseb(x)))
            if c == 7:
                m.append(n.copy())
                n = []
                c = 0

    m.append(n)
    return m


def btn_buy(typ):
    global wybrany
    cuser = mod.load(get_cookie('login'))
    x = wybrany
    if typ == 'Kup':
        close_popup()
        cuser.rc -= prices[x]
        cuser.avatar.append(x)
        toast(f'Kupiono {x}!')
        mod.save(cuser)
        run_js('window.location.reload()')


def buy(x):
    cuser = mod.load(get_cookie('login'))
    global wybrany
    wybrany = x
    if cuser.rc < prices[x]:
        toast(f'Nie masz tyle remicoinów!')
    else:
        popup(f'Kupić {x} za {prices[x]}?', [
            put_buttons(['Kup'], onclick=btn_buy)

        ])


def choosed(x):
    cuser = mod.load(get_cookie('login'))
    toast(f'Wybrano {x}')
    cuser.pfp = x
    mod.save(cuser)
    run_js('window.location.reload()')


def chooseb(x):
    cuser = mod.load(get_cookie('login'))
    toast(f'Wybrano {x}')
    cuser.badge = x
    mod.save(cuser)
    run_js('window.location.reload()')


def choose_badge(passed):
    cuser = mod.load(get_cookie('login'))
    if passed.nick == cuser.nick:
        popup('Wybierz Odznake', [
            put_grid(badgen2(), cell_width='65px', cell_height='65px')

        ])


def choose_avatar(passed):
    cuser = mod.load(get_cookie('login'))
    if passed.nick == cuser.nick:
        popup('Wybierz Avatar', [
            put_grid(imggen(), cell_width='65px', cell_height='65px')

        ])


def store():
    cuser = mod.load(get_cookie('login'))

    put_row([
        put_buttons(['Back'], onclick=btn_clk),
        put_text(f"RemiCoins: {cuser.rc}").style(
            f'font-size: 25px; font-family: "Comic Sans MS", "Chalkboard SE", "Comic Neue", sans-serif; color: red')
    ])
    put_grid(imggen2(), cell_width='65px', cell_height='65px')


def addbadge():
    userki = []

    users = os.listdir('users')

    for x in users:
        userki.append((x.split('.')[0]))

    odznaki = []

    name = select('Podaj Nick', userki, required=True)
    u = mod.load(name)
    for x in badges.keys():
        if x not in u.badges:
            odznaki.append(x)
    bg = select('Podaj Odznake', odznaki, required=True)
    u.badges.append(bg)
    u.titles.append(avtitles[bg])
    mod.save(u)
    panel()


def addRMC():
    userki = []

    users = os.listdir('users')

    for x in users:
        userki.append((x.split('.')[0]))

    name = select('Podaj Nick', userki, required=True)
    rm = int(input('Podaj ilosc rmc', required=True))

    u = mod.load(name)
    u.rc += rm
    mod.save(u)


def showbadges():
    put_buttons(['Back'], onclick=btn_clk)
    put_row([
        put_grid(badgen3(), cell_width='65px', cell_height='65px')
    ])


def despedit():
    cuser = mod.load(get_cookie('login'))
    desp = input('Wprowadz opis')
    cuser.huj['desp'] = desp
    mod.save(cuser)
    run_js('window.location.reload()')


def tytch(x):
    cuser = mod.load(get_cookie('login'))
    cuser.title = x
    mod.save(cuser)
    run_js('window.location.reload()')


def tytgen():
    cuser = mod.load(get_cookie('login'))
    m = []
    n = []
    c = 0
    for x in avtitles.values():
        if x in cuser.titles:
            c += 1
            n.append(put_text(f'{x}').onclick(lambda x=x: tytch(x)).style(f'text-align: center;'))
            if c == 7:
                m.append(n.copy())
                n = []
                c = 0

    m.append(n)
    return m


def title():
    popup('Wybierz Tytul', [
        put_grid(tytgen(), cell_width='65px', cell_height='65px')

    ])


def add_role():
    rola = input('Podaj nazwe roli', required=True)
    roles = read_roles()
    if rola in roles:
        popup('Istnieje juz ta rola!')
        add_role()
    else:
        mod.add_data("roles", rola)
        clear()
        panel()


def add_postac():
    postac = input('Podaj nazwe postaci', required=True)
    postacie = read_postacie()
    if postac in postacie:
        popup('Istnieje juz ta postac!')
        add_postac()
    else:
        mod.add_data("postacie", postac)
        clear()
        panel()

### ---------------------------------------------------------------------------------------
#                                   Wordly
### ---------------------------------------------------------------------------------------

def wordly_buttoms(typ):
    if typ == 'Wróć do danmmaku':
        clear()
        panel()
    elif typ == 'Statystyki graczy':
        clear()
        wordly_panel_players()


def wordly_panel_players():
    userki = []

    users = os.listdir('users')

    for x in users:
        userki.append(mod.load(x.split('.')[0]))

    userki.sort(key=lambda y: y.won, reverse=True)
    style_row_head = f'font-size: 25px; font-family: Helvetica, Arial, sans-serif; margin: auto; text-align: center; font-weight: bold'
    put_buttons(['Wordly'],onclick=btn_clk).style(style_row_head)
    put_row([
        put_text(f'Avatar').style(style_row_head),
        put_text(f'Title').style(style_row_head),
        put_text(f'Nazwa').style(style_row_head),
        put_text(f'Zgadnietych').style(style_row_head),
        put_text(f'Najwiekszy Streak').style(style_row_head),
        put_text(f'Aktualny Streak').style(style_row_head),
    ])
    style_rows_content = f'font-size: 25px; font-family: Helvetica, Arial, sans-serif; margin: auto; text-align: center'
    for h in range(0, len(userki)):
        x = userki[h]
        put_row([
            put_image(pictures[x.pfp], width='75px', height='75px').style(style_rows_content),
            put_text(f'{x.title}').style(style_rows_content),
            put_text(f'{x.nick}').style(style_rows_content),
            put_text(x.wordly_won).style(style_rows_content),
            put_text(x.wordly_max_streak).style(style_rows_content),
            put_text(x.wordly_cur_streak).style(style_rows_content),

        ])



def wordly_panel():
    clear()
    style_text = f'font-size: 25px; font-family: Helvetica, Arial, sans-serif; margin: auto; text-align: center'
    cuser = mod.load(get_cookie('login'))
    if not checklogin(cuser):
        return
    put_column([
        put_scope('Top'),
        put_scope('Content'),
    ],size = 'auto auto')
    with use_scope('Top'):
        put_row([
            put_column([
                put_buttons(['Wróć do danmmaku'], onclick=wordly_buttoms).style(f'margin: auto'),
                put_buttons(['Statystyki graczy'], onclick=wordly_buttoms).style(f'margin: auto')
            ]),
            put_column([
                put_buttons(['Store'], onclick=btn_clk).style(f'margin: auto'),
                put_buttons(['BadgeList'], onclick=btn_clk).style(f'margin: auto')
            ]),
            put_column([
                put_buttons(['Title'], onclick=btn_clk).style(f'margin: auto'),
                put_buttons(['Description'], onclick=btn_clk).style(f'margin: auto')
            ]),
            put_text(f'{cuser.title}\n{cuser.nick}').style(style_text),
            put_image(pictures[cuser.pfp], width=f'100px', height=f'100px').onclick(lambda: choose_avatar(cuser)),
            put_text(f"RemiCoins: {cuser.rc}").style(
                f'font-size: 25px; font-family: Helvetica, Arial, sans-serif; color: red; margin: auto')

        ],size='auto auto auto auto auto auto')
        try:
            desc = cuser.huj['desp']
        except:
            desc = f'Brak opisu'
        put_row([
                put_image(badges[cuser.badge], width=f'100px', height=f'100px').onclick(
                    lambda: choose_badge(cuser)).style(
                    f'margin: 10px'),
                put_text(desc).style(f'font-size: 20px; font-family: Helvetica, Arial, sans-serif; margin: auto')
            ],size = 'auto auto')


    wordly_update_content()

def wordly_select_vali(data):
    global characters_names
    user = mod.load(get_cookie('login'))
    if not checklogin(user):
        return
    if not data['name'] in characters_names:
        return ('name','Nie poprawna nazwa postaci!')
    our_tries = []
    for x in user.wordly_tries:
        our_tries.append(x.name[0])
    if data['name'] in our_tries:
        return ('name','Dzisiaj już zgadywałeś ta postać!')


def wordly_create_try_helper(today, our):
    wrong = f'color: red'
    something = f'color: orange'
    good = f'color: green'

    have = len(today)
    our_have = len(our)
    agreed = 0
    for y in today:
        for z in our:
            if z == y:
                agreed += 1

    entire_string = ''
    for x in our:
        entire_string+= ' '+x

    if agreed == have and have == our_have:
        return [entire_string.strip(), good]
    elif agreed > 0 :
        return [entire_string.strip(), something]
    else:
        return  [entire_string.strip(),wrong]
def wordly_create_try():
    style_text = f'font-size: 25px; font-family: Helvetica, Arial, sans-serif; margin: 5px; text-align: center'

    user = mod.load(get_cookie('login'))
    if not checklogin(user):
        return
    today_character = wordly.get_today_character()
    data = []
    for x in user.wordly_tries:
        data_row = []
        data_row.append(wordly_create_try_helper(today_character.name, x.name))
        data_row.append(wordly_create_try_helper(today_character.race, x.race))
        data_row.append(wordly_create_try_helper(today_character.home, x.home))
        data_row.append(wordly_create_try_helper(today_character.first, x.first))
        data_row.append(wordly_create_try_helper(today_character.head, x.head))
        data_row.append(wordly_create_try_helper(today_character.hair, x.hair))
        data_row.append(wordly_create_try_helper(today_character.atrb, x.atrb))
        data.append(data_row)

    data_final = []
    data_final.append([put_text('Obraz', scope='Content').style(style_text).style(f'font-weight: bold'),
        put_text('Nazwa', scope='Content').style(style_text).style(f'font-weight: bold'),
        put_text('Rasa', scope='Content').style(style_text).style(f'font-weight: bold'),
        put_text('Lokacja', scope='Content').style(style_text).style(f'font-weight: bold'),
        put_text('Pierwsze wystąpienie', scope='Content').style(style_text).style(f'font-weight: bold'),
        put_text('Nakrycie głowy', scope='Content').style(style_text).style(f'font-weight: bold'),
        put_text('Kolor włosów', scope='Content').style(style_text).style(f'font-weight: bold'),
        put_text('Atrybut', scope='Content').style(style_text).style(f'font-weight: bold')])

    for x in data:
        data_final.append([
                put_image(wordly_pictures[x[0][0].strip()], scope='Content').style(style_text),
                put_text(x[0][0], scope='Content').style(style_text).style(x[0][1]),
                put_text(x[1][0], scope='Content').style(style_text).style(x[1][1]),
                put_text(x[2][0], scope='Content').style(style_text).style(x[2][1]),
                put_text(x[3][0], scope='Content').style(style_text).style(x[3][1]),
                put_text(x[4][0], scope='Content').style(style_text).style(x[4][1]),
                put_text(x[5][0], scope='Content').style(style_text).style(x[5][1]),
                put_text(x[6][0], scope='Content').style(style_text).style(x[6][1])
        ])
    put_grid(data_final).style(style_text)






def wordly_check_for_character(char):
    global characters
    user = mod.load(get_cookie('login'))
    if not checklogin(user):
        return
    today_character = wordly.get_today_character()
    our_character = []
    for c in characters:
        if char['name'] == c.name[0]:
            our_character = c
            break
    user.wordly_tries.append(our_character)
    if our_character.name[0] == today_character.name[0]:
        user.wordly_win_today = True
        user.wordly_win = True
        num = len(user.wordly_tries)
        rm = user.wordly_cur_streak
        if num < 6:
            rm += 20
        elif num < 11:
            rm += 15
        elif num < 21:
            rm += 10
        else:
            rm += 5
        user.rc += rm
        user.wordly_cur_streak+=1
        if user.wordly_cur_streak > user.wordly_max_streak:
            user.wordly_max_streak = user.wordly_cur_streak
        user.wordly_won +=1
        popup('Zgadleś postać!','Jest to twoja '+str(user.wordly_won)+' zgadnięta postać\nTwoja aktualna seria zgadniętych postaci pod rząd to '+str(user.wordly_cur_streak)+'\nZgadłeś '+str(today_character.name[0])+' po '+str(len(user.wordly_tries))+' próbach za co otrzymujesz: '+str(rm)+' RemiCoinów')
    mod.save(user)
    #wordly_update_content()
    wordly_panel()


def wordly_update_content():
    clear('Content')
    style_text = f'font-size: 35px; font-family: Helvetica, Arial, sans-serif; margin: auto; text-align: center'
    global characters
    characters = wordly.get_characters()
    global characters_names
    characters_names = []
    for x in characters:
        characters_names.append(x.name[0])

    user = mod.load(get_cookie('login'))
    if not checklogin(user):
        return
    wordly_create_try()
    if not user.wordly_win_today:
        character_choice = input_group('Zgadnij dzisiejszą Touhou postać!',[input('Wybierz postać' ,  name='name' ,datalist= characters_names)],validate=wordly_select_vali)
        wordly_check_for_character(character_choice)

def wordly_reset():
    while True:
        users = os.listdir('users')
        for x in users:
            u = mod.load(x.split('.')[0])
            if u.wordly_win_today == False:
                u.wordly_cur_streak = 0
            u.wordly_tries = []
            u.wordly_win_today = False
            u.wordly_win = False
            mod.save(u)
        wordly.new_wordly()
        time.sleep(10)

if __name__ == '__main__':


    start_server(cope, port=80, debug=True)




