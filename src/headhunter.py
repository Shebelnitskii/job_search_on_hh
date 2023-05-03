import requests


class HeadHunterAPI():
    def __init__(self):
        self.url_vacancies = f"https://api.hh.ru/vacancies"  # URL API HeadHunter

    def get_vacancies(self, employer_id, limit_vacancy, specialization=None, exp=None):
        """
        Метод для получения вакансий с помощью API SuperJob.

        employer_id id работодателя
        return Список объектов класса Vacancy.
        """
        page = 0
        vacancies = []
        employers = []
        while True:
            params = {"per_page": 100, "employer_id": employer_id,  ### id работодателя
                      # 'specialization': 1, 'experience': exp,  ### код отрасли (IT, компьютеры, связь)
                      'page': page}
            response_vacancy = requests.get(self.url_vacancies, params=params)
            if response_vacancy.ok:
                data_vacancy = response_vacancy.json()
                vacancies_data = data_vacancy['items']
                for vacancy in vacancies_data:
                    if len(vacancies) >= limit_vacancy:
                        break
                    salary_data = vacancy['salary']
                    try:
                        if salary_data['to'] == None:  ### Проверка на диапазон зарплаты
                            salary = {'from': salary_data['from'], 'to': 0, 'currency': salary_data['currency']}
                        elif salary_data['from'] == None:
                            salary = {'from': 0, 'to': salary_data['to'], 'currency': salary_data['currency']}
                        else:
                            salary = {'from': salary_data['from'], 'to': salary_data['to'],
                                      'currency': salary_data['currency']}
                    except (KeyError, TypeError):
                        salary = {'from': 0, 'to': 0, 'currency': 'RUR'}  ### Если зарплата не указано то в значение фром сохраняется нулевое значение
                    vacancy = {'id': vacancy['id'],
                               'job_title': vacancy['name'],  ### Название вакансии
                               'salary_from': salary['from'],
                               'salary_to': salary['to'],
                               'currency': salary['currency'],
                               'description': vacancy['snippet']['requirement'],  ### Описание вакансии
                               'area': vacancy['area']['name'],
                               'id_employer': vacancy['employer']['id'],
                               'employer': vacancy['employer']['name'],
                               'url': vacancy['alternate_url'],  ### url ссылка на вакансию
                               'date': vacancy['published_at']}  ### дата публикации вакансии
                    if not any(vacancy['id'] == v['id'] for v in vacancies):
                        vacancies.append(vacancy)
                if page >= data_vacancy['pages'] - 1 or len(vacancies) >= limit_vacancy:
                    break
                page += 1

            else:
                break


        response_employers = requests.get(f'https://api.hh.ru/employers/{employer_id}')
        if response_employers.ok:
            data_employer = response_employers.json()
            employer = {'id_company': data_employer['id'],
                        'employer_name': data_employer['name'],
                        'description': data_employer['description'],
                        'site': data_employer['site_url']}
            if employer not in employers:
                employers.append(employer)

        return vacancies, employers
