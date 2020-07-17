import os
import xml.etree.ElementTree as ET
import datetime
import config
import csv

def main():
    all_categories = []
    folder = os.path.join('.', 'data')
    start_time = datetime.datetime.now()
    all_output = []
    with open(os.path.join('.', 'categories_data.csv'), 'w', newline='') as csvfile:
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
                statistics = boardgame.find('statistics')
                ratings = statistics.find('ratings')
                bayesaverage = ratings.find('bayesaverage')
                bayes_rating = float(bayesaverage.text)
                if bayes_rating==0:
                    continue
                categories = boardgame.findall('boardgamecategory')
                categories_values = []
                for category in all_categories:
                    categories_values.append(0)
                for category in categories:
                    if category.text not in all_categories:
                        all_categories.append(category.text)
                        categories_values.append(1)
                    else:
                        categories_values[all_categories.index(category.text)] = 1
                output = []
                output.append(bayes_rating)
                for element in categories_values:
                    output.append(element)
                all_output.append(output)
        header_output = ['bayes_rating']
        for element in all_categories:
            header_output.append(element)
        csv_writer.writerow(header_output)
        for element in all_output:
            while len(element)<len(all_categories)+1:
                element.append(0)
            csv_writer.writerow(element)

if __name__ == '__main__':
    main()
