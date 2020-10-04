import sys
from datetime import date
import pandas as pd
import requests
import json


def problems_with_json(func):
    def wrapper(*args):
        try:
            func(*args)
        except:
            print("problems with {}".format(func.__name__))
    return wrapper


def text_slice(start_str, end_str, text):
    text = text[text.find(start_str) + len(start_str):]
    text = text[:text.find(end_str)].strip()
    return text


from_str_date_to_date = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }


class Covid():

    def __init__(self, country):
        self.country = country
        url = f'https://www.worldometers.info/coronavirus/country/{self.country.strip().lower()}/'
        self.source = requests.get(url)

        self.time = []
        self.total_cases = []
        self.daily_cases = []
        self.total_currently_infected = []
        self.total_death = []
        self.death_per_day = []
        self.new_recoveries = []

    def get_datetime_from_str_day(self):
        for i in range(len(self.time)):
            self.time[i] = date(2020, from_str_date_to_date[self.time[i][:3]], int(self.time[i][-2:]))

    def get_time(self):
        total_cases_time = text_slice("text: 'Total Cases'", "yAxis: {", self.source.text)
        total_cases_time = text_slice("categories:", "},", total_cases_time)
        self.time = json.loads(total_cases_time)
        self.get_datetime_from_str_day()

    @problems_with_json
    def get_total_cases(self):
        total_cases = text_slice("name: 'Cases',", "responsive: {", self.source.text)
        total_cases = text_slice("data:", "}],", total_cases)
        self.total_cases = json.loads(total_cases.replace('null', '0'))

    @problems_with_json
    def get_daily_cases(self):
        daily_cases = text_slice("name: 'Daily Cases',", "},", self.source.text)
        daily_cases += ';'
        daily_cases = text_slice("data: ", ";", daily_cases)
        self.daily_cases = json.loads(daily_cases.replace('null', '0'))

    @problems_with_json
    def get_total_currently_infected(self):
        total_currently_infected = text_slice("name: 'Currently Infected'", "}", self.source.text)
        total_currently_infected += ";"
        total_currently_infected = text_slice("data: ", ";", total_currently_infected)
        self.total_currently_infected = json.loads(total_currently_infected.replace('null', '0'))

    @problems_with_json
    def get_total_death(self):
        total_death = text_slice("name: 'Deaths',", "],", self.source.text)
        total_death = text_slice("data: ", "}", total_death)
        self.total_death = json.loads(total_death.replace('null', '0'))

    @problems_with_json
    def get_death_per_day(self):
        death_per_day = text_slice("name: 'Daily Deaths'", "}", self.source.text)
        death_per_day += ";"
        death_per_day = text_slice("data: ", ";", death_per_day)
        self.death_per_day = json.loads(death_per_day.replace('null', '0'))

    @problems_with_json
    def get_new_recoveries(self):
        new_recoveries = text_slice("name: 'New Recoveries'", "}", self.source.text)
        new_recoveries += ";"
        new_recoveries = text_slice("data: ", ";", new_recoveries)
        self.new_recoveries = json.loads(new_recoveries.replace('null', '0'))

    def write_to_csv(self):
        df = pd.DataFrame()
        for key, value in self.__dict__.items():
            if issubclass(type(value), list) and len(value):
                df[key] = value
        df.to_csv(f'{self.__class__.__name__}{self.country.capitalize()}.csv', index=False)


def main():
    country = sys.argv[1]

    data = Covid(country)
    try:
        data.get_time()
    except :
        print("probably, invalid link (country)")
        return
    data.get_total_cases()
    data.get_daily_cases()
    data.get_total_currently_infected()
    data.get_total_death()
    data.get_death_per_day()
    data.get_new_recoveries()

    data.write_to_csv()


if __name__ == '__main__':
    main()