import csv
import random
import pandas
import numpy as np
import matplotlib.pyplot as plt  # To visualize
from sklearn.linear_model import LinearRegression

def main():
    dtypes = {
        'bayes_rating': float
    }
    headers = []
    with open('subdomain_data.csv') as data:
        csvreader = csv.reader(data)
        for row in csvreader:
            header = row
            for entry in header:
                if entry not in dtypes:
                    dtypes[entry] = bool
                    headers.append(entry)
            break
    data = pandas.read_csv('subdomain_data.csv', dtype=dtypes)
    columns = []
    for i in range(8):
        columns.append('bayes_rating')
    Y = data[columns].values.reshape(-1, 8)
    data = data.drop(columns=['bayes_rating'])
    X = data.values.reshape(-1,8)
    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(X, Y)  # perform linear regression
    coefs = linear_regressor.coef_[0]
    highest_coefs = [-1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000]
    best_coefs = [-1, -1, -1, -1, -1, -1, -1, -1]
    for repeat in range(20):
        for i in range(8):
            for j in range(8):
                if coefs[i] > highest_coefs[j] and i not in best_coefs:
                    highest_coefs[j] = coefs[i]
                    best_coefs[j] = i
    output = {}
    for j in range(8):
        output[headers[best_coefs[j]]] = highest_coefs[j]
    for key in output:
        print(f'{key}: {output[key]}')

if __name__=='__main__':
    main()
