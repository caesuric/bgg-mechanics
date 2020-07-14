import requests
import time
import os
import sys
import config

def main():
    make_folder()
    missed_count = 0
    for i in range(config.max_game):
        print (f'{round(i/config.max_game * 100, 2)}% done')
        response = requests.get(f'https://www.boardgamegeek.com/xmlapi/boardgame/{i}?stats=1')
        if response.status_code == 404:
            missed_count += 1
            if missed_count >= 1000:
                break
        elif response.status_code != 200:
            time.sleep(5)
            i -= 1
        else:
            with open(os.path.join('.', 'data', f'game{i}.xml'), 'wb') as xml_file:
                # print(response.text)
                xml_file.write(response.text.encode(sys.stdout.encoding, errors='replace'))

def make_folder():
    if os.path.isdir(os.path.join('.', 'data')):
        return
    os.mkdir(os.path.join('.', 'data'))

if __name__=='__main__':
    main()