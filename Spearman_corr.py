import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta, datetime
from scipy.stats import spearmanr
import argparse
import sys
import os
import json
from numpy import inf


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

    args = parser.parse_args()

    try:
        countries_raw = args.countries
        country_list = countries_raw.split(",")
    except Exception:
        sys.exit("QUIT: countries parameter are not in correct format")

    return country_list, args.file_path


class Spearman(object):
    def __init__(self, country, file_path):
        self.country = country
        self.file_path = file_path

    def train(self):
        """ Retrieve Covid Data """
        file_name = str(self.file_path).capitalize()
        try:
            covid_country_info = pd.read_csv(file_name)
        except:
            sys.exit("There is no file {} -- train func // country".format(file_name))

        death = covid_country_info['death_per_day'].values
        infected = covid_country_info['daily_cases'].values
        covid_date = covid_country_info['time'].values

        """ Retrieve Restrictions Data """
        restr_file = "all_restrictions/Stringency{}.csv".format(str(self.country).capitalize())
        try:
            stringency_country_info = pd.read_csv(restr_file)
        except:
            print("There is no file {} -- train func // all_restrictions".format(file_name))
            return
            
        index = stringency_country_info['Stringency Index (OxBSG)'].values

        """ Time Lag 14 Days """
        values = []
        stringency_date = stringency_country_info['Date'].values
        for i in range(len(stringency_date)):
            current = datetime.strptime(stringency_country_info.iloc[i]['Date'], '%Y-%m-%d')
            str_date = np.array([datetime.strftime(current, '%Y-%m-%d')])
            current = current - timedelta(days=14)
            values.append(datetime.strftime(current, '%Y-%m-%d'))

        """ Merging Data """
        df_covid = pd.DataFrame(
            {'date': covid_date,
             'infected': infected,
             'death': death,
             })
        df_covid['infected'] = df_covid['infected'].pct_change()
        df_covid['death'] = df_covid['death'].pct_change()
        df_covid = df_covid.fillna(0)
        df_covid = df_covid.replace(np.inf, 1)

        df_stringency = pd.DataFrame(
            {'date': values,
             'index': index,
             })

        df_covid = df_covid.merge(right=df_stringency.reset_index(drop=True), how='left', on='date')

        """ Checking Correlation """
        coef_inf, p_inf = spearmanr(df_covid['infected'].values, df_covid['index'].values, nan_policy='omit')
        print('INFECTED -- Spearmans correlation coefficient: %.3f' % coef_inf)
        print('INFECTED -- Spearmans correlation p-value: %.3f' % p_inf)

        coef_death, p_death = spearmanr(df_covid['death'].values, df_covid['index'].values, nan_policy='omit')
        print('DEATH -- Spearmans correlation coefficient: %.3f' %coef_death)
        print('DEATH -- Spearmans correlation p-value: %.3f' %p_death)

        data = {'Infection_corr_index': coef_inf,
                'Infection_p-value': p_inf,
                'Death_corr_index': coef_death,
                'Death_p-value': p_death}

        fig, ax = plt.subplots()
        ax.scatter(df_covid['infected'].values, df_covid['index'].values)
        ax.set_title(self.country)
        ax.set_xlabel("infected")
        ax.set_ylabel("stringency index")

        fig_d, ax_d = plt.subplots()
        ax_d.scatter(df_covid['death'].values, df_covid['index'].values)
        ax_d.set_title(self.country)
        ax_d.set_xlabel("death")
        ax_d.set_ylabel("stringency index")

        folder_path = f'Spearman/{self.country}/'
        os.makedirs(folder_path, exist_ok=True)
        with open(folder_path + f'Spearman{self.country}.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        fig.savefig(folder_path + f"infected{self.country}.png")
        fig_d.savefig(folder_path + f"death{self.country}.png")


def main():
    countries, file_path = parse_arguments()

    for country in countries:
        spearman_corr = Spearman(country, file_path)
        spearman_corr.train()


if __name__ == '__main__':
    main()
