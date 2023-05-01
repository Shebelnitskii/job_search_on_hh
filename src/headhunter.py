import requests


class HeadHunterAPI():
    def __init__(self):
        self.url_vacancies = f"https://api.hh.ru/vacancies"  # URL API HeadHunter

    def get_vacancies(self, employer_id):
        """
        Метод для получения вакансий с помощью API SuperJob.

        exp Опыт работы.
        key_word Ключевое слово для поиска вакансии.
        return Список объектов класса Vacancy.
        """
        page = 0
        vacancies = []
        employers = []
        while True:
            params = {"per_page": 100, "employer_id": employer_id,  ### id работодателя
                      'specialization': 1,  ### код отрасли (IT, компьютеры, связь)
                      'page': page}
            response_vacancy = requests.get(self.url_vacancies, params=params)
            response_employers = requests.get(f'https://api.hh.ru/employers/{employer_id}')
            if response_vacancy.ok:
                if response_employers.ok:
                    data_vacancy = response_vacancy.json()
                    data_employer = response_employers.json()
                    vacancies_data = data_vacancy['items']
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
                                   'date': vacancy['published_at']}  ### дата публикации вакансии
                        employer = {'id_vacancy': vacancy['id'],
                                    'id_company': data_employer['id'],
                                    'employer_name': data_employer['name'],
                                    'description': data_employer['description'],
                                    'site': data_employer['site_url']}
                        vacancies.append(vacancy)
                        employers.append(employer)
                    if page >= data_vacancy['pages'] - 1:
                        break
                    page += 1
                else:
                    break
            else:
                break
        return vacancies, employers

