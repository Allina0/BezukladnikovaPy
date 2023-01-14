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
        self.dataFrame = pd.read_csv(VACANCIES_FILE, usecols=['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name'])
        self.dataFrame['average'] = self.dataFrame[['salary_from', 'salary_to']].mean(axis=1)
        self.dataFrame['salary'] = self.dataFrame.apply(self.get_salary, axis=1)
        self.dataFrame.dropna(subset=['salary'], inplace=True)


        new_dataFrame = pd.DataFrame({'salary': self.dataFrame.groupby(['area_name'])['salary'].mean()}).reset_index()
        new_dataFrame = new_dataFrame.sort_values(by=['salary'], ascending=False)[1:21]

        new_dataFrame2 = pd.DataFrame({'count': self.dataFrame.groupby(['area_name']).size()}).reset_index()
        new_dataFrame2 = new_dataFrame2.sort_values(by=['count'], ascending=False).head(20)
        count = self.dataFrame.shape[0]
        new_dataFrame2['part'] = new_dataFrame2['count'].apply(lambda c: round(c / count, 4))


        print(new_dataFrame)
        print(new_dataFrame2)

        fig, axes = plt.subplots(nrows=1, ncols=1)
        axes.bar(new_dataFrame['area_name'].to_list(), new_dataFrame['salary'].to_list())
        axes.set_title('Уровень зарплат по городам (в порядке убывания)')
        axes.set_ylabel('Зарплата, руб.')
        axes.set_xlabel('Город')
        plt.xticks(rotation=90)
        plt.tight_layout()
        fig.savefig('image_5.png')

        fig, axes = plt.subplots(nrows=1, ncols=1)
        axes.bar(new_dataFrame2['area_name'].to_list(), new_dataFrame2['part'].to_list())
        axes.set_title('Доля вакансий по городам (в порядке убывания)')
        axes.set_ylabel('Доля вакансий')
        axes.set_xlabel('Город')
        plt.xticks(rotation=90)
        plt.tight_layout()
        fig.savefig('image_6.png')

    @staticmethod
    def get_salary(row):
        try:
            return row['average'] * currency_to_rub[row['salary_currency']]
        except:
            return np.nan


if __name__ == '__main__':
    demand = Demand()
