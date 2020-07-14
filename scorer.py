import requests
import os
import config
import xml.etree.ElementTree as ET

def main():
    all_mechanics = {}
    folder = os.path.join('.', 'data')
    for i in range(config.max_game):
        filename = os.path.join(folder, f'game{i}.xml')
        if os.path.isfile(filename):
            xml_tree = ET.parse(filename)
            boardgame = xml_tree.find('boardgame')
            error = boardgame.find('error')
            if error is not None:
                continue
            statistics = boardgame.find('statistics')
            ratings = statistics.find('ratings')
            ranks = ratings.find('ranks')
            rank = ranks.findall('rank')
            for rank_obj in rank:
                if rank_obj.get('name') == 'boardgame':
                    rank_value = int(rank_obj.get('value'))
                    if rank_value <= 1000:
                        average = ratings.find('average')
                        game_rating = float(average.text)
                        mechanics = boardgame.findall('boardgamemechanic')
                        for mechanic in mechanics:
                            if mechanic not in all_mechanics:
                                all_mechanics[mechanic.text] = game_rating
                            else:
                                all_mechanics[mechanic.text] += game_rating
    print_mechanics(all_mechanics)

def print_mechanics(mechanics):
    list_format =[k + ': ' + str(v) for k, v in sorted(mechanics.items(), reverse=True, key=lambda item: item[1])]
    for item in list_format:
        print(item)

if __name__=='__main__':
    main()