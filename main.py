from pywebio.input import input, FLOAT, input_group, NUMBER, PASSWORD, select, checkbox
from pywebio.output import put_text, put_row, put_code, put_buttons, clear, popup, remove, put_scope, put_image, toast, \
    put_column, put_table
from pywebio import start_server, config
from pywebio.session import run_js
from pywebio_battery import get_cookie, set_cookie
import os
import mod

logged = False

roles = ['Heroine', 'Rival', 'Partner', 'EX Midboss', 'One True Partner', 'Stage Boss', 'Final Boss', 'Challenger',
         'Anti-Heroine', 'EX Boss', 'Phantasm Boss', 'Secret Boss', 'Lone Wolf', 'Mob Boss', 'Back Stage Boss']

postacie = ['Aki Minoriko', 'Alice Margatroid', 'Chen', 'Cirno', 'Clownpiece', 'Doremy Sweet', 'Eternity Larva', 'Flandre Scarlet', 'Fujiwara no Mokou', 'Futatsuiwa Mamizou', 'Hakurei Reimu', 'Hata no Kokoro', 'Hecatia Lapislazuli', 'Hijiri Byakuren', 'Hinanawi Tenshi', 'Hong Meiling', 'Horikawa Raiko', 'Hoshiguma Yuugi', 'Houjuu Nue', 'Houraisan Kaguya', 'Ibuki Suika', 'Imaizumi Kagerou', 'Izayoi Sakuya', 'Junko', 'Kaenbyou Rin', 'Kagiyama Hina', 'Kaku Seiga', 'Kamishirasawa Keine', 'Kasodani Kyouko', 'Kawashiro Nitori', 'Kazami Yuuka', 'Kijin Seija', 'Kirisame Marisa', 'Kishin Sagume', 'Kochiya Sanae', 'Komano Aun', 'Komeiji Koishi', 'Komeiji Satori', 'Konpaku Youmu', 'Kumoi Ichirin', 'Kurodani Yamame', 'Letty Whiterock', 'Mizuhashi Parsee', 'Mononobe no Futo', 'Moriya Suwako', 'Mystia Lorelei', 'Nagae Iku', 'Nazrin', 'Onozuka Komachi', 'Patchouli Knowledge', 'Prismriver Sisters', 'Reisen Udongein Inaba', 'Reiuji Utsuho', 'Remilia Scarlet', 'Rumia', 'Saigyouji Yuyuko', 'Seiran', 'Sekibanki', 'Shameimaru Aya', 'Shiki Eiki', 'Sukuna Shinmyoumaru', 'Tatara Kogasa', 'Toramaru Shou', 'Toyosatomimi no Miko', 'Usami Sumireko', 'Wakasagihime', 'Wriggle Nightbug', 'Yagokoro Eirin', 'Yakumo Ran', 'Yakumo Yukari', 'Yasaka Kanako', 'Yorigami Joon & Shion']


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

    if lose+twins == 0:
        sumka = 1
    else:
        sumka = lose+twins
    wr = round((twins/sumka)*100, 2)


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
            put_text(f'Śmierdzi: {deaths}'),
            put_text(f'Gier Totalnie: {twins+lose}'),
            put_text(f'W/R: {wr}%')
        ]).style(f'font-size: 25px; font-family: "Comic Sans MS", "Chalkboard SE", "Comic Neue", sans-serif; line-height: 0.8'),

        put_text(f'Congratulation no badge given')
    ])
    put_row([
        put_table([roles,s]).style(f'width: 100%;')
    ]).style(f'padding-top: 35px;')
    put_row([
        put_text(f'HISTORIA GIER').style(f'font-size: 35px; font-family: "Comic Sans MS", "Chalkboard SE", "Comic Neue", sans-serif; line-height: 0.8')
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

    ]).style(f'font-size: 20px; font-family: "Comic Sans MS", "Chalkboard SE", "Comic Neue", sans-serif; line-height: 3')


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

    for h in range(0,len(userki)):
        x = userki[h]
        put_row([

            put_image(pictures[x.pfp], width='50px', height='50px'),
            put_text(f'{x.nick}').onclick(lambda x=x: panel(x)),
            put_text(x.twins)

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
        select('Podaj Postac', postacie, name= 'postac', required=True),
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



