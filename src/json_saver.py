import json

class JSONSaver:
    def __init__(self):
        self.file_name_vacancy: str = 'JSON_vacancy.json'
        self.file_name_employers: str = 'JSON_employers.json'

    def add_vacancies(self, vacancyes, employers):
        """
        Сохраняет информацию о вакансиях в файл JSON.

        Аргументы:
        headhunter: Список вакансий с сайта HeadHunter.
        """
        with open(self.file_name_vacancy, 'w', encoding='utf-8') as file:
            json.dump(vacancyes,file, ensure_ascii=False, indent=4)
        with open(self.file_name_employers, 'w', encoding='utf-8') as file:
            json.dump(employers,file, ensure_ascii=False, indent=4)