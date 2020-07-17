import requests
import time
import os
import sys
import config
import datetime

def main():
    start_time = datetime.datetime.now()
    make_folder()
    missed_count = 0
    for i in range(253103,config.max_game):
        current_time = datetime.datetime.now()
        seconds_passed = (current_time-start_time).total_seconds()
        total_seconds = (config.max_game-253103) / float(i+1-253103) * seconds_passed
        print(f'{round((i-253103)/(config.max_game-253103) * 100, 2)}% done, {total_seconds-seconds_passed} seconds remain')
        response = requests.get(f'https://www.boardgamegeek.com/xmlapi/boardgame/{i}?stats=1')
        if response.status_code == 404:
            missed_count += 1
            if missed_count >= 1000:
                break
        elif response.status_code != 200:
            time.sleep(5)
            i -= 1
        else:
            missed_count = 0
            with open(os.path.join('.', 'data', f'game{i}.xml'), 'wb') as xml_file:
                # print(response.text)
                xml_file.write(response.text.encode(sys.stdout.encoding, errors='replace'))

def make_folder():
    if os.path.isdir(os.path.join('.', 'data')):
        return
    os.mkdir(os.path.join('.', 'data'))

if __name__=='__main__':
    main()