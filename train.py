import pandas as pd
from config import *
import numpy as np
import matplotlib.pyplot as plt
import argparse

def EstimatePrice(mileage, th0, th1):
    return (th0 + (th1 * mileage))

def calc_precision(data, th0, th1):
    prediction = EstimatePrice(data['km'], th0, th1)
    abs_diff = [x if x > 0 else -x for x in prediction - data['price']]
    mean = sum(map(float,abs_diff))
    return mean

def normalize_data(df):
    mins = {'km': 0, 'price': 0}   
    maxs = {'km': 0, 'price': 0}   
    for column_name in df.columns:
        col = df[column_name]
        mins[column_name] = col.min()
        maxs[column_name] = col.max()
        df[column_name] = [(x - mins[column_name]) / maxs[column_name] for x in col]

    return df, mins, maxs

def unnormalize_data(df, mins, maxs):
    for column_name in df.columns:
        df[column_name] = [x * maxs[column_name] + mins[column_name] for x in col]
    return df 

def train(args):
    raw_data = pd.read_csv("data.csv", delimiter= ',')

    th0 = 0
    th1 = 0

    data, mins, maxs = normalize_data(raw_data.copy())

    precision = np.array([])
    thetas = np.array([])

    for i in range(EPOCHS):
        tmpth0 = EstimatePrice(data['km'], th0, th1) - data['price']
        tmpth1 = (EstimatePrice(data['km'], th0, th1) - data['price']) * data['km']

        th0 -= tmpth0.mean() * LEARNING_RATE
        th1 -= tmpth1.mean() * LEARNING_RATE
        precision = np.append(precision, calc_precision(data, th0, th1))
        if i == 0:
            thetas = np.array([[th0, th1]])
        else:
            thetas = np.append(thetas, [[th0, th1]], axis=0)

    best_epoch = precision.argmin()
    th0 = thetas[best_epoch, 0]
    th1 = thetas[best_epoch, 1]

    prediction = EstimatePrice(data['km'], th0, th1)

    if args.plot:
        plt.plot(raw_data['km'], prediction * maxs['price'] + mins['price'], label="prediction")
        plt.plot(raw_data['km'], raw_data['price'], 'o', label="raw data")
        plt.xlabel('km')
        plt.ylabel('price')
        plt.legend()
        plt.savefig("prices.png")

        plt.clf()
        plt.axvline(x = best_epoch, color = 'r', alpha=0.5, label = 'best epoch')
        plt.plot(range(len(precision)), precision * maxs['price'] + mins['price'], '.',
            label="error evolution")
        plt.xlabel('epochs')
        plt.ylabel('precision')
        plt.legend()
        plt.savefig("model_evolution.png")

    if not args.noout:
        with open("thetas.txt", "w") as file:
            file.write("{}\n{}\n{} - {}\n{} - {}\n".format(th0, th1,
                mins['km'], mins['price'], maxs['km'], maxs['price']))

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--noout", action="store_true", help="add for no output")
    parser.add_argument("-p", "--plot", action="store_true", help="show plots")
    args = parser.parse_args()
    return args

if __name__ == '__main__': 
    args = get_arguments()
    train(args)