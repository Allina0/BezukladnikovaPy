from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('require/', demand, name='demand'),
    path('location/', geography, name='geography'),
    path('experience/', skills, name='skills'),
    path('last_vacancies/', vacancies, name='vacancies'),
]
