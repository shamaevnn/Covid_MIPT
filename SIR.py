import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta, datetime
from scipy.integrate import odeint
from scipy.optimize import minimize
from population_dict import population_dict
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
        '--file-path',
        required=False,
        dest='file_path',
        help='Destination to file with covid info. Default is Data/Covid',
        metavar='FILE_PATH',
        type=str,
        default="Data/Covid")

    parser.add_argument(
        '--prediction-days',
        required=False,
        dest='predict_range',
        help='Days to predict with the model. Defaults to 140',
        metavar='PREDICT_RANGE',
        type=int,
        default=140)

    args = parser.parse_args()

    try:
        countries_raw = args.countries
        country_list = countries_raw.split(",")
    except Exception:
        sys.exit("QUIT: countries parameter are not in correct format")

    return country_list, args.file_path, args.predict_range


def extend_index(country_name: str, new_size, file_path):
    file_name = "{}{}.csv".format(file_path, country_name.capitalize())
    try:
        data = pd.read_csv(file_name)
        current = datetime.strptime(data.iloc[0]['time'], '%Y-%m-%d')
        values = np.array([datetime.strftime(current, '%Y-%m-%d')])
        while len(values) < new_size:
            current = current + timedelta(days=1)
            values = np.append(values, datetime.strftime(current, '%Y-%m-%d'))

        return values
    except:
        sys.exit("There is no file {} -- extend_index func".format(file_name))


def SIR(state, t, N, beta, gamma):
    """N - population of country"""
    S, I, R = state

    dSdt = -beta * S * I / N

    dIdt = beta * S * I / N - gamma * I

    dRdt = gamma * I

    return dSdt, dIdt, dRdt


class Learner(object):
    def __init__(self, country_name, file_path, loss, predict_range):
        self.country = country_name
        self.file_path = file_path
        self.loss = loss
        self.predict_range = predict_range
        self.i_0 = 2
        self.r_0 = 0
        try:
            self.s_0 = population_dict[str(self.country).capitalize()] * 2 / 1000
        except:
            sys.exit("No info about population for {} in population_dict.py".format(self.country))

    def predict(self, beta, gamma, infected, recovered, death, country, s_0, i_0, r_0):
        new_index = extend_index(country, self.predict_range, self.file_path)
        size = len(new_index)

        extended_actual = np.concatenate((infected, [None] * (size - len(infected))))
        extended_recovered = np.concatenate((recovered, [None] * (size - len(recovered))))
        extended_death = np.concatenate((death, [None] * (size - len(death))))

        S, I, R = odeint(SIR, [s_0, i_0, r_0], range(0, size), args=(s_0, beta, gamma)).T

        return new_index, extended_actual, extended_recovered, extended_death, S, I, R

    def train(self):
        file_name = "{}{}.csv".format(self.file_path, str(self.country).capitalize())
        try:
            covid_country_info = pd.read_csv(file_name)
        except:
            sys.exit("There is no file {} -- train func".format(file_name))
        death = covid_country_info['total_death'].values
        infected = covid_country_info['total_currently_infected'].values
        total_cases = covid_country_info['total_cases'].values
        recovered = total_cases - infected

        optimal = minimize(loss, [0.4, 0.05], args=(infected, recovered, self.s_0, self.i_0, self.r_0),
                           method='L-BFGS-B', bounds=[(0.00000001, 0.4), (0.00000001, 0.4)])

        #
        beta, gamma = optimal.x

        new_index, extended_actual, extended_recovered, extended_death, S, I, R = self.predict(beta, gamma, infected,
                                                                                               recovered, death,
                                                                                               self.country,
                                                                                               self.s_0, self.i_0,
                                                                                               self.r_0)

        df = pd.DataFrame(
            {'Infected data': extended_actual[:self.predict_range],
             'Recovered data': extended_recovered[:self.predict_range],
             'I': I, 'R': R
             })

        data = {'fact_infected': list(extended_actual[:self.predict_range]),
                'fact_recovered': list(extended_recovered[:self.predict_range]), 'predicted_infected': list(I),
                'predicted_recovered': list(R), 'params': {'beta': beta, 'gamma': gamma}}

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_title(self.country)
        df.plot(ax=ax)
        print(f"country={self.country}, beta={beta:.8f}, gamma={gamma:.8f}, r_0:{(beta / gamma):.8f}")

        folder_path = f'SIR/{self.country}/'
        os.makedirs(folder_path, exist_ok=True)
        with open(folder_path + f'data.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        fig.savefig(folder_path + f"{self.country}.png")


def loss(point, infected, recovered, s_0, i_0, r_0):
    size = len(infected)
    beta, gamma = point

    S, I, R = odeint(SIR, [s_0, i_0, r_0], range(0, size), args=(s_0, beta, gamma)).T
    l1 = np.sqrt(np.mean((I - infected) ** 2) / len(I))
    l2 = np.sqrt(np.mean((R - recovered) ** 2) / len(R))
    alpha = 0.8
    return alpha * l1 + (1 - alpha) * l2


def main():
    countries, file_path, predict_range = parse_arguments()

    for country in countries:
        learner = Learner(country, file_path, loss, predict_range)
        learner.train()


if __name__ == '__main__':
    main()
