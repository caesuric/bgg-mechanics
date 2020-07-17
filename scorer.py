import requests
import os
import xml.etree.ElementTree as ET
import datetime
import config
import csv

def main():
    all_mechanics = {}
    mechanic_counts = {}
    folder = os.path.join('.', 'data')
    start_time = datetime.datetime.now()
    for i in range(config.max_game):
        current_time = datetime.datetime.now()
        seconds_passed = (current_time-start_time).total_seconds()
        total_seconds = config.max_game / float(i+1) * seconds_passed
        print(
            f'{round(i/config.max_game * 100, 2)}% done, {total_seconds-seconds_passed} seconds remain')
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
                    if rank_obj.get('value')=='Not Ranked':
                        continue
                    rank_value = int(rank_obj.get('value'))
                    if rank_value <= 1000:
                        average = ratings.find('average')
                        game_rating = float(average.text)
                        mechanics = boardgame.findall('boardgamemechanic')
                        for mechanic in mechanics:
                            if mechanic.text not in all_mechanics:
                                all_mechanics[mechanic.text] = game_rating
                                mechanic_counts[mechanic.text] = 1
                            else:
                                all_mechanics[mechanic.text] += game_rating
                                mechanic_counts[mechanic.text] += 1
    print_mechanics(all_mechanics, mechanic_counts)

def print_mechanics(mechanics, mechanic_counts):
    for element in mechanics:
        mechanics[element] /= mechanic_counts[element]
    list_format =[[k,v] for k, v in sorted(mechanics.items(), reverse=True, key=lambda item: item[1])]
    for item in list_format:
        print(item)
    with open('mechanics-scores.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for item in list_format:
            csv_writer.writerow(item)

if __name__=='__main__':
    main()
