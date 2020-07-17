import csv
import random
import pandas
import numpy as np
import matplotlib.pyplot as plt  # To visualize
from sklearn.linear_model import LinearRegression

def main():
    dtypes = {
        'rating': float,
        'bayes_rating': float
    }
    headers = []
    with open('all_data.csv') as data:
        csvreader = csv.reader(data)
        for row in csvreader:
            header = row
            for entry in header:
                if entry not in dtypes:
                    dtypes[entry] = bool
                    headers.append(entry)
            break
    data = pandas.read_csv('all_data.csv', dtype=dtypes)
    columns = []
    for i in range(182):
        columns.append('bayes_rating')
    Y = data[columns].values.reshape(-1, 182)
    # X = data[['Singing', 'Legacy Game']].values.reshape(-1, 2)
    data = data.drop(columns=['bayes_rating', 'rating'])
    X = data.values.reshape(-1,182)
    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(X, Y)  # perform linear regression
    # Y_pred = linear_regressor.predict(X)  # make predictions
    # plt.scatter(X, Y)
    # plt.plot(X, Y_pred, color='red')
    # plt.show()

    # highest_rating = 0
    # while True:
    #     new_data = []
    #     for i in range(182):
    #         new_data.append(0)
    #     for i in range(5):
    #         roll = random.randint(0,181)
    #         new_data[roll] = 1
    #     rating = linear_regressor.predict([new_data])[0][0]
    #     if rating > highest_rating:
    #         highest_rating = rating
    #         print('-------------------------------')
    #         print(f'New winner! - {highest_rating}')
    #         print('Mechanics:')
    #         for i in range(182):
    #             if new_data[i]==1:
    #                 print(headers[i])

    coefs = linear_regressor.coef_[0]
    highest_coefs = [-1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000]
    best_coefs = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    for repeat in range(20):
        for i in range(182):
            for j in range(10):
                if coefs[i] > highest_coefs[j] and i not in best_coefs:
                    highest_coefs[j] = coefs[i]
                    best_coefs[j] = i
    output = {}
    for j in range(10):
        output[headers[best_coefs[j]]] = highest_coefs[j]
    for key in output:
        print(f'{key}: {output[key]}')

    # values = []
    # for i in range(182):
    #     if headers[i] in ['Order Counters', 'Turn Order: Pass Order', 'Auction: Dutch', 'Delayed Purchase', 'Advantage Token']:
    #         values.append(1)
    #     else:
    #         values.append(0)
    # rating = linear_regressor.predict([values])[0][0]
    # print(rating)

    # values = []
    # for i in range(182):
    #     if headers[i] in ['Legacy Game', 'Resource to Move', 'Turn Order: Pass Order', 'Critical Hits and Failures', 'Advantage Token']:
    #         values.append(1)
    #     else:
    #         values.append(0)
    # rating = linear_regressor.predict([values])[0][0]
    # print(rating)


if __name__=='__main__':
    main()
