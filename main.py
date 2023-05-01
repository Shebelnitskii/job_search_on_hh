from src.headhunter import HeadHunterAPI
from src.json_saver import JSONSaver
import requests
import json

employers_id = [1740, 78638, 3529, 733, 67611, 15478, 851604, 2686590, 80, 9418714]
employer_id = '78638'
hh_api = HeadHunterAPI()
hh_vacancies, hh_employers = hh_api.get_vacancies(employer_id)
json_saver = JSONSaver()  ### Создание объекта для сохранения результатов в JSON-файл
json_saver.add_vacancies(hh_vacancies, hh_employers)

