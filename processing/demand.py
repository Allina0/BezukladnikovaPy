import numpy as np
import requests
from lxml import etree
import matplotlib.pyplot as plt

import pandas as pd


currency_to_rub = {
    "AZN": 35.68, "BYR": 23.91, "EUR": 59.90, "GEL": 21.74, "KGS": 0.76,
    "KZT": 0.13, "RUR": 1, "UAH": 1.64, "USD": 60.66, "UZS": 0.0055,
}

VACANCIES_FILE = './data/vacancies_with_skills.csv'


class Demand:
    def __init__(self):
        self.dataFrame = pd.read_csv(VACANCIES_FILE, usecols=['name', 'salary_from', 'salary_to', 'salary_currency', 'published_at'])
        self.dataFrame['average'] = self.dataFrame[['salary_from', 'salary_to']].mean(axis=1)
        self.dataFrame['salary'] = self.dataFrame.apply(self.get_salary, axis=1)
        self.dataFrame['date'] = self.dataFrame.apply(self.get_date, axis=1)
        self.dataFrame['year'] = self.dataFrame.apply(self.get_year, axis=1)
        self.dataFrame.dropna(subset=['salary'], inplace=True)

        dataFrame2 = self.dataFrame[self.dataFrame['name'].str.contains('|'.join(['PHP-программист', 'php']), case=False)]

        new_dataFrame = pd.DataFrame()

        new_dataFrame['salary'] = self.dataFrame.groupby(['year'])['salary'].mean()
        new_dataFrame['count'] = self.dataFrame.groupby(['year']).size()

        new_dataFrame['s_salary'] = dataFrame2.groupby(['year'])['salary'].mean()
        new_dataFrame['s_count'] = dataFrame2.groupby(['year']).size()
        print(new_dataFrame)

        stats = new_dataFrame.to_dict()

        fig, axes = plt.subplots(nrows=1, ncols=1)
        axes.bar(list(stats['salary'].keys()), list(stats['salary'].values()))
        axes.set_title('Динамика уровня зарплат по годам')
        axes.set_ylabel('Зарплата, руб.')
        axes.set_xlabel('Год')
        plt.xticks(rotation=90)
        plt.tight_layout()
        fig.savefig('image_3.png')

        fig, axes = plt.subplots(nrows=1, ncols=1)
        axes.bar(list(stats['count'].keys()), list(stats['count'].values()))
        axes.set_title('Динамика количества вакансий по годам')
        axes.set_ylabel('Кол-во вакансий')
        axes.set_xlabel('Год')
        plt.xticks(rotation=90)
        plt.tight_layout()
        fig.savefig('image_2.png')

        fig, axes = plt.subplots(nrows=1, ncols=1)
        axes.bar(list(stats['s_salary'].keys()), list(stats['s_salary'].values()))
        axes.set_title('Динамика уровня зарплат по годам для выбранной профессии')
        axes.set_ylabel('Зарплата, руб.')
        axes.set_xlabel('Год')
        plt.xticks(rotation=90)
        plt.tight_layout()
        fig.savefig('image_3.png')

        fig, axes = plt.subplots(nrows=1, ncols=1)
        axes.bar(list(stats['s_count'].keys()), list(stats['s_count'].values()))
        axes.set_title('Динамика количества вакансий по годам для выбранной профессии')
        axes.set_ylabel('Кол-во вакансий')
        axes.set_xlabel('Год')
        plt.xticks(rotation=90)
        plt.tight_layout()
        fig.savefig('image_4.png')

    @staticmethod
    def get_salary(row):
        try:
            return row['average'] * currency_to_rub[row['salary_currency']]
        except:
            return np.nan

    @staticmethod
    def get_date(row):
        return row['published_at'][:7]

    @staticmethod
    def get_year(row):
        return row['published_at'][:4]


if __name__ == '__main__':
    demand = Demand()
