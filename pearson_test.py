import json
from scipy.stats import chisquare
from scipy.stats import chi2
import scipy.stats as stats
import numpy as np
import argparse
import sys
import os


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

    args = parser.parse_args()

    try:
        countries_raw = args.countries
        country_list = countries_raw.split(",")
    except Exception:
        sys.exit("QUIT: countries parameter are not in correct format")

    return country_list


class Pearson(object):
    def __init__(self, country):
        self.country = country


    def train(self):
        file_name = "SIR/{}/data.json".format(str(self.country))
        try:
            with open(file_name) as json_file:
                data = json.load(json_file)
        except:
            print("There is no file {} -- train func".format(file_name))
            return

        """ Deleted the first day to get rid of ZEROs """
        inf_fact_data = np.asarray(data['fact_infected'][1:])
        inf_pred_data = np.asarray(data['predicted_infected'][1:])
        rec_fact_data = np.asarray(data['fact_recovered'][1:])
        rec_pred_data = np.asarray(data['predicted_recovered'][1:])

        """ Degrees of freedom """
        df_inf = len(inf_fact_data) - 1
        df_rec = len(rec_fact_data) - 1

        """ Scaling data """
        inf_fact_data_sc = inf_fact_data / inf_fact_data.std()
        inf_pred_data_sc = inf_pred_data / inf_pred_data.std()
        rec_fact_data_sc = rec_fact_data / rec_fact_data.std()
        rec_pred_data_sc = rec_pred_data / rec_pred_data.std()


        """ Scipy calculations """
        chi_inf = chisquare(f_obs=inf_fact_data_sc, f_exp=inf_pred_data_sc)
        chi_rec = chisquare(f_obs=rec_fact_data_sc, f_exp=rec_pred_data_sc)
        print("Infected -- χ² statistic, p-value: ", chi_inf)
        print("Recovered -- χ² statistic, p-value: ", chi_rec)

        critical_value = stats.chi2.ppf(q=0.95, df=df_inf)
        print("Critical value: ", critical_value)

        if chi_inf.statistic > critical_value:
            infected_validation = False
        else:
            infected_validation = True

        if chi_rec.statistic > critical_value:
            recovered_validation = False
        else:
            recovered_validation = True

        fin_data = {
            'critical_value': critical_value,
            'infected_statistic': chi_inf.statistic,
            'recovered_statistic': chi_rec.statistic,
            'infected_validation': infected_validation,
            'recovered_validation': recovered_validation
            }

        folder_path = f"SIR/{self.country}/"
        os.makedirs(folder_path, exist_ok=True)
        with open(folder_path + f'PearsonSIR{self.country}.json', 'w') as outfile:
            json.dump(fin_data, outfile, indent=4)


def main():
    countries = parse_arguments()

    for country in countries:
        validation = Pearson(country)
        validation.train()


if __name__ == '__main__':
    main()
