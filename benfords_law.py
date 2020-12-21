import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta, datetime
from scipy.integrate import odeint
from scipy.optimize import minimize
from population_dict import population_dict
from scipy.stats import chisquare
import scipy.stats as stats
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
    def __init__(self, country, file_name):
        self.country = country
        self.file_name = file_name

    def train(self):
        try:
            covid_country_info = pd.read_csv(str(self.file_name).capitalize())
        except:
            print("File error")
            sys.exit("There is no file {} -- train func".format(file_name))

        death_per_day = covid_country_info['death_per_day'].values
        total_currently_infected = covid_country_info['total_currently_infected'].values
        daily_cases = covid_country_info['daily_cases'].values

        folder_path = f"Benfords_law/{self.country}/"
        os.makedirs(folder_path, exist_ok=True)

        labels = []
        for i in range(1, 10):
            labels.append(str(i))
        benfords_law_distribution = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]

        death_distribution = distribution_of_digits(death_per_day)
        infected_distribution = distribution_of_digits(total_currently_infected)
        daily_cases_distribution = distribution_of_digits(daily_cases)

        x = np.arange(len(labels)) 
        width = 0.6
        fig, ax = plt.subplots()
        ax.plot(benfords_law_distribution, color='#00D0D0', linewidth=6, label="Benford's law")
        ax.bar(x - width/3, daily_cases_distribution, width/3, label="Daily cases")
        ax.bar(x, infected_distribution, width/3, label="Infected")
        ax.bar(x + width/3, death_distribution, width/3, label="Daily death cases")

        ax.set_ylabel('First digit distribution')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()

        plt.title(self.country) 
        
        fig.savefig(folder_path + f"{self.country}.png")

        #   Pearson test
        daily_cases_len = len(daily_cases)
        total_currently_infected_len = len(total_currently_infected)
        death_per_day_len = len(death_per_day)
        
        daily_cases_inf = chisquare(f_obs=daily_cases_distribution*daily_cases_len,
                                    f_exp=benfords_law_distribution*daily_cases_len)
        infected_inf = chisquare(f_obs=infected_distribution*total_currently_infected_len,
                                    f_exp=benfords_law_distribution*total_currently_infected_len)
        daily_death_inf = chisquare(f_obs=death_distribution*death_per_day_len,
                                    f_exp=benfords_law_distribution*death_per_day_len)

        df = len(benfords_law_distribution) - 1
        critical_value = stats.chi2.ppf(q=0.99, df=df)
        print("Critical value: ", critical_value)

        daily_cases_validation = False if daily_cases_inf.statistic > critical_value else True
        infected_validation = False if infected_inf.statistic > critical_value else True
        daily_death_validation = False if daily_death_inf.statistic > critical_value else True

        fin_data = {
            'critical_value': critical_value,
            'daily_cases_statistic': daily_cases_inf.statistic,
            'infected_statistic': infected_inf.statistic,
            'daily_death_statistic': daily_death_inf.statistic,
            'daily_cases_validation': infected_validation,
            'infected_validation': daily_death_validation,
            'daily_death_validation': daily_cases_validation,
            }

        os.makedirs(folder_path, exist_ok=True)
        with open(folder_path + f'PearsonBenfordsLaw{self.country}.json', 'w') as outfile:
            json.dump(fin_data, outfile, indent=4)
        

#   TODO: It does not work for common program - needs to be discussed
# def main():
#     countries, predict_range = parse_arguments()

#     for country in countries:
#         benford = Benfords_law(country)
#         benford.train()

# if __name__ == '__main__':
#     main()
