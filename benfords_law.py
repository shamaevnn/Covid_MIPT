import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta, datetime
from scipy.integrate import odeint
from scipy.optimize import minimize
from population_dict import population_dict
from scipy.stats import chisquare
import argparse
import sys
import os
import json


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--countries',
        action='store',
        dest='countries',
        help='Name of country/countries separated by comma without spaces' +
             'It must exact match the data names or you will get out of bonds error.',
        metavar='COUNTRY_NAMES',
        type=str,
        default="")

    parser.add_argument(
        '--prediction-days',
        required=False,
        dest='predict_range',
        help='Days to predict with the model. Defaults to 150',
        metavar='PREDICT_RANGE',
        type=int,
        default=140)

    args = parser.parse_args()

    try:
        countries_raw = args.countries
        country_list = countries_raw.split(",")
    except Exception:
        sys.exit("QUIT: countries parameter are not in correct format")

    return country_list, args.predict_range


def first_digit(number):
    while number > 9:
        number //= 10
    return number


def distribution_of_digits(array):
    distribution_count = [0] * 10
    for number in array:
        distribution_count[first_digit(number)] += 1
    size = len(array)
    distribution = []
    for count in distribution_count:
        distribution.append(count / size)
    distribution.pop(0)
    return distribution


class Benfords_law(object):
    def __init__(self, title, file_name):
        self.title = title
        self.file_name = file_name

    def train(self):
        try:
            covid_country_info = pd.read_csv(str(self.file_name).capitalize())
        except:
            print("File error")
            sys.exit("There is no file {} -- train func".format(file_name))

        death = covid_country_info['total_death'].values
        infected = covid_country_info['total_currently_infected'].values
        total_cases = covid_country_info['total_cases'].values
        daily_cases = covid_country_info['daily_cases'].values
        recovered = total_cases - infected

        folder_path = f"Benfords_law/{self.title}/"
        os.makedirs(folder_path, exist_ok=True)

        labels = []
        for i in range(1, 10):
            labels.append(str(i))
        benfords_law_distribution = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]

        total_cases_distribution = distribution_of_digits(total_cases)
        infected_distribution = distribution_of_digits(infected)
        daily_cases_distribution = distribution_of_digits(daily_cases)

        x = np.arange(len(labels)) 
        width = 0.4
        fig, ax = plt.subplots()
        ax.plot(benfords_law_distribution, color='#00D0D0', linewidth=6, label="Benford's law")
        ax.bar(x + width/2, daily_cases_distribution, width, label="Daily cases")
        ax.bar(x - width/2, infected_distribution, width, label="Infected")

        ax.set_ylabel('First digit distribution')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()

        plt.title(self.title) 
        
        fig.savefig(folder_path + f"{self.title}.png")

#   TODO: upload data to csv
        daily_cases_inf = chisquare(f_obs=daily_cases_distribution, f_exp=benfords_law_distribution)
        print("daily cases -- χ² statistic, p-value: ", daily_cases_inf)

#   TODO: It does not work for common program - needs to be discussed
# def main():
#     countries, predict_range = parse_arguments()

#     for country in countries:
#         benford = Benfords_law(country)
#         benford.train()


# if __name__ == '__main__':
#     main()
