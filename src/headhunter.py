import requests


class HeadHunterAPI():
    def __init__(self):
        self.url = f"https://api.hh.ru/vacancies"  # URL API HeadHunter

    def get_class_vacancies(self):
        """
        Метод для получения вакансий с помощью API SuperJob.

        exp Опыт работы.
        key_word Ключевое слово для поиска вакансии.
        return Список объектов класса Vacancy.
        """
        params = {"text": "IT",
                  "employer_id": 3529, ### id работодателя
                  'specialization': 1} ### код отрасли (IT, компьютеры, связь)
        # headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(self.url, params=params)
        if response.ok:
            data = response.json()
            vacancies_data = data['items']
            vacancies = []
            for vacancy in vacancies_data:
                title = vacancy['name']  ### Название вакансии
                salary_data = vacancy['salary']
                try:
                    if salary_data['to'] == None:  ### Проверка на диапазон зарплаты
                        salary = {'from': salary_data['from'], 'currency': salary_data['currency']}
                    elif salary_data['from'] == None:
                        salary = {'from': salary_data['to'], 'currency': salary_data['currency']}
                    else:
                        salary = {'from': salary_data['from'], 'to': salary_data['to'],
                                  'currency': salary_data['currency']}
                except:
                    salary = {'from': 0,
                              'currency': 'RUR'}  ### Если зарплата не указано то в значение фром сохраняется нулевое значение
                description = vacancy['snippet']['requirement']  ### Описание вакансии
                employer = vacancy['employer']['name']
                url = vacancy['alternate_url']  ### url ссылка на вакансию
                vacancy = {'title': title,
                           'salary': salary,
                           'description': description,
                           'employ': employer,
                           'url': url}
                vacancies.append(vacancy)
            return vacancies
        else:
            vacancies = []
            return vacancies
