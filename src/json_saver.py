import json

class JSONSaver:
    def __init__(self):
        self.file_name: str = 'JSON.json'

    def add_vacancies(self, headhunter=None):
        """
        Сохраняет информацию о вакансиях в файл JSON.

        Аргументы:
        headhunter: Список вакансий с сайта HeadHunter.
        """
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(
                sorted([vacancy for vacancy in headhunter], key=lambda x: x['salary']['from'], reverse=True),
                file, ensure_ascii=False, indent=4)
