import os
import xml.etree.ElementTree as ET
import datetime
import config
import csv

def main():
    folder = os.path.join('.', 'data')
    start_time = datetime.datetime.now()
    all_output = []
    with open(os.path.join('.', 'basic_data.csv'), 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        for i in range(config.max_game):
            current_time = datetime.datetime.now()
            seconds_passed = (current_time-start_time).total_seconds()
            total_seconds = config.max_game / float(i+1) * seconds_passed
            print(f'{round(i/config.max_game * 100, 2)}% done, {total_seconds-seconds_passed} seconds remain')
            filename = os.path.join(folder, f'game{i}.xml')
            if os.path.isfile(filename):
                xml_tree = ET.parse(filename)
                boardgame = xml_tree.find('boardgame')
                error = boardgame.find('error')
                if error is not None:
                    continue
                yearpublished = 'Unknown'
                if boardgame.find('yearpublished') is not None:
                    yearpublished = boardgame.find('yearpublished').text
                minplayers = 'Unknown'
                maxplayers = 'Unknown'
                playingtime = 'Unknown'
                minplaytime = 'Unknown'
                maxplaytime = 'Unknown'
                age = 'Unknown'
                if boardgame.find('minplayers') is not None:
                    minplayers = boardgame.find('minplayers').text
                if boardgame.find('maxplayers') is not None:
                    maxplayers = boardgame.find('maxplayers').text
                if boardgame.find('playingtime') is not None:
                    playingtime = boardgame.find('playingtime').text
                if boardgame.find('minplaytime') is not None:
                    minplaytime = boardgame.find('minplaytime').text
                if boardgame.find('maxplaytime') is not None:
                    maxplaytime = boardgame.find('maxplaytime').text
                if boardgame.find('age') is not None:
                    age = boardgame.find('age').text
                names = boardgame.findall('name')
                name = ''
                for name_obj in names:
                    if 'primary' in name_obj.attrib and name_obj.attrib['primary']=='true':
                        name = name_obj.text
                        break
                description = boardgame.find('description').text
                thumbnail = ''
                image = ''
                if boardgame.find('thumbnail') is not None:
                    thumbnail = boardgame.find('thumbnail').text
                if boardgame.find('image') is not None:
                    image = boardgame.find('image').text
                statistics = boardgame.find('statistics')
                ratings = statistics.find('ratings')
                average = ratings.find('average')
                game_rating = float(average.text)
                bayesaverage = ratings.find('bayesaverage')
                bayes_rating = float(bayesaverage.text)
                usersrated = int(ratings.find('usersrated').text)
                stddev = float(ratings.find('stddev').text)
                owned = int(ratings.find('owned').text)
                trading = int(ratings.find('trading').text)
                wanting = int(ratings.find('wanting').text)
                wishing = int(ratings.find('wishing').text)
                numweights = int(ratings.find('numweights').text)
                averageweight = float(ratings.find('averageweight').text)
                ranks = ratings.find('ranks')
                rank_objs = ranks.findall('rank')
                bggrank = 'Not Ranked'
                for rank in rank_objs:
                    if rank.attrib['name']=='boardgame':
                        bggrank = rank.attrib['value']
                output = []
                output.append(name)
                output.append(description)
                output.append(thumbnail)
                output.append(image)
                output.append(game_rating)
                output.append(bayes_rating)
                output.append(usersrated)
                output.append(bggrank)
                output.append(stddev)
                output.append(owned)
                output.append(trading)
                output.append(wanting)
                output.append(wishing)
                output.append(numweights)
                output.append(averageweight),
                output.append(yearpublished)
                output.append(minplayers)
                output.append(maxplayers)
                output.append(playingtime)
                output.append(minplaytime)
                output.append(maxplaytime)
                output.append(age)
                all_output.append(output)
        header_output = ['name', 'description', 'thumbnail', 'image', 'rating', 'bayes_rating', 'usersrated', 'bggrank', 'stddev', 'owned', 'trading', 'wanting', 'wishing', 'numweights', 'averageweight', 'yearpublished', 'minplayers', 'maxplayers', 'playingtime', 'minplaytime', 'maxplaytime', 'age']
        csv_writer.writerow(header_output)
        for element in all_output:
            csv_writer.writerow(element)

if __name__ == '__main__':
    main()
