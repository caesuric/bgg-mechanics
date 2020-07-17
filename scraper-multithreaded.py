import requests
import time
import os
import sys
import datetime
import threading
import config
from multiprocessing import Process

def main():
    make_folder()
    start = 254021
    for i in range(start, start+8):
        p = Process(target=run_thread, args=(i,))
        p.start()

def run_thread(i):
    while i <= config.max_game:
        get_game(i)
        i += 1

def get_game(i):
    if os.path.isfile(os.path.join('.', 'data', f'game{i}.xml')):
        return
    try:
        response = requests.get(f'https://www.boardgamegeek.com/xmlapi/boardgame/{i}?stats=1')
    except:
        get_game(i)
    if response.status_code != 200:
        time.sleep(5)
        get_game(i)
    else:
        with open(os.path.join('.', 'data', f'game{i}.xml'), 'wb') as xml_file:
            xml_file.write(response.text.encode(sys.stdout.encoding, errors='replace'))

def make_folder():
    if os.path.isdir(os.path.join('.', 'data')):
        return
    os.mkdir(os.path.join('.', 'data'))

if __name__=='__main__':
    main()
