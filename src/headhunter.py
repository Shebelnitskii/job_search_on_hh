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
        params = {"employer_id": 733,  ### id работодателя
                  'specialization': 1}  ### код отрасли (IT, компьютеры, связь)
        # headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(self.url, params=params)
        if response.ok:
            data = response.json()
            vacancies_data = data['items']
            vacancies = []
            employers = []
            for vacancy in vacancies_data:
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
                vacancy = {'id': vacancy['id'],
                           'job_title': vacancy['name'],  ### Название вакансии
                           'salary': salary,
                           'description': vacancy['snippet']['requirement'],  ### Описание вакансии
                           'area': vacancy['area'],
                           'employer': vacancy['employer']['name'],
                           'url': vacancy['alternate_url'],  ### url ссылка на вакансию
                           'date': vacancy['published_at']} ### дата публикации вакансии
                employer = {'id_vacancy': vacancy['id'],
                            'id_company': vacancy['employer']['id'],
                            'employer_name': vacancy['employer']['name']
                            }
                vacancies.append(vacancy)
                employers.append(employer)
            return vacancies, employers
        else:
            vacancies = []
            employers = []
            return vacancies, employers
