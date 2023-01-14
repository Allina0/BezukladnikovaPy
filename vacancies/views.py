import datetime
import requests

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import *


links = [
    {
        'title': 'Главная',
        'name': 'home',
    },
    {
        'title': 'Востребованность',
        'name': 'demand',
    },
    {
        'title': 'География',
        'name': 'geography',
    },
    {
        'title': 'Навыки',
        'name': 'skills',
    },
    {
        'title': 'Последние вакансии',
        'name': 'vacancies',
    }
]


class HH:
    def __init__(self, items):
        self.items = items

    class HHVacancy:
        def __init__(self, name, description, experience_skill, employer, area, salary, published_at):
            self.name = name
            self.description = description
            self.skills = experience_skill
            self.employer = employer
            self.area = area
            self.salary = salary
            self.published_at = published_at

    def make_vacancy(self):
        vacancy_list = []
        for item in self.items:
            accord = requests.get(f'https://api.hh.ru/vacancies/{item["id"]}').json()
            if len(accord['key_skills']) == 0:
                experience_skill = 'Не указаны'
            else:
                experience_skill = '<ol>'
                experience_skill += ''.join(map(lambda skill: '<li>' + skill['name'] + '</li>', accord['key_skills']))
                experience_skill += '</ol>'
            if not accord['salary']:
                salary = 'Не указана'
            else:
                if accord['salary']['from'] and accord['salary']['to']:
                    salary = (accord['salary']['from'] + accord['salary']['to']) / 2
                elif accord['salary']['from'] and not accord['salary']['to']:
                    salary = accord['salary']['from']
                elif not accord['salary']['from'] and accord['salary']['to']:
                    salary = accord['salary']['to']
                else:
                    salary = 'Не указана'
            date = '{0[2]}.{0[1]}.{0[0]}'.format(accord['published_at'][:10].split('-'))
            vacancy_list.append(self.HHVacancy(accord['name'], accord['description'], experience_skill, accord['employer']['name'], accord['area']['name'], salary, date))
        return vacancy_list


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'vacancies/home.html', {
        'title': links[0]['title'],
        'links': links,
    })


def demand(request: HttpRequest) -> HttpResponse:
    return render(request, 'vacancies/demand.html', {
        'title': links[1]['title'],
        'links': links,
        'types': Type.objects.all(),
    })


def geography(request: HttpRequest) -> HttpResponse:
    return render(request, 'vacancies/geography.html', {
        'title': links[2]['title'],
        'links': links,
        'types': Type.objects.all(),
    })


def skills(request: HttpRequest) -> HttpResponse:
    return render(request, 'vacancies/skills.html', {
        'title': links[3]['title'],
        'links': links,
        'types': Type.objects.all(),
    })


def vacancies(request: HttpRequest) -> HttpResponse:
    response = requests.get('https://api.hh.ru/vacancies?specialization=1&per_page=10&page=1&date_from=2022-12-16T00:00:00&date_to=2022-12-16T23:59:59&text=NAME:(php)')
    json = response.json()['items']
    hh = HH(json)
    return render(request, 'vacancies/vacancies.html', {
        'title': links[4]['title'],
        'links': links,
        'items': hh.make_vacancy()
    })
