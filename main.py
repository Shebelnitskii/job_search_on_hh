from src.headhunter import HeadHunterAPI
from src.json_saver import JSONSaver
import json

# hh_api = HeadHunterAPI()
# hh_vacancies, hh_employers = hh_api.get_class_vacancies()
# json_saver = JSONSaver()  ### Создание объекта для сохранения результатов в JSON-файл
# json_saver.add_vacancies(hh_vacancies, hh_employers)

import requests

employer_id = '733'
response = requests.get(f'https://api.hh.ru/employers/{employer_id}')
data = response.json()
with open('employers.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)