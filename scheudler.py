import main
import datetime
import time


while True:
    now = datetime.datetime.now()
    cas = now.strftime('%H:%M')
    if cas == '02:00':
        main.wordly_reset()
    time.sleep(59)
    print(cas)
