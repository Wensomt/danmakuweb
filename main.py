from pywebio.input import input, FLOAT, input_group, NUMBER, PASSWORD
from pywebio.output import put_text, put_row, put_code, put_buttons, clear, popup
from pywebio import start_server, config
from pywebio.session import run_js
from pywebio_battery import get_cookie, set_cookie
import mod

logged = False





def btn_clk(typ):
    if logged == False:
        if typ == 'Login':
            clear()
            cope()
            loginf()
        elif typ == 'Register':
            clear()
            cope()
            register()

@config(theme="dark")
def cope():
    global cuser
    login = get_cookie('login')
    passwd = get_cookie('passwd')

    print(login)
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
    ])
    u = mod.User(info['name'], info['pswd'])
    if mod.save(u):
        popup('Nick w uzyciu!')
    else:
        clear()

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


def panel():
    global cuser
    put_text(f'Zalogowano jako {cuser.nick}')


if __name__ == '__main__':

    start_server(cope, port=80, debug=True)



