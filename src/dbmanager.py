import psycopg2


class DBManager:
    def __init__(self, host, database, user, password):
        self.conn = psycopg2.connect(host=host, database=database, user=user, password=password)

    def get_companies_and_vacancies_count(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT employers.employer_name, COUNT(vacancy.id) as count_vacancies
                FROM vacancy JOIN employers ON vacancy.id_employer = employers.id_company
                GROUP BY employers.employer_name
                """
            )
            results = cur.fetchall()
            for row in results:
                company, count = row
                print(f'В компании {company} {count} вакансий')

    def get_all_vacancies(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT employers.employer_name, vacancy.job_title, vacancy.salary_from, vacancy.salary_to, 
                vacancy.currency, vacancy.url
                FROM vacancy JOIN employers ON vacancy.id_employer = employers.id_company
                """
            )
            results = cur.fetchall()
            for row in results:
                employer_name, job_title, salary_from, salary_to, currency, url = row
                if salary_from == 0 and salary_to == 0:
                    print(
                        f'Вакансия: {job_title} от {employer_name} \nЗарплата не указана\nСсылка:{url}\n')
                elif salary_from == 0:
                    print(
                        f'Вакансия: {job_title} от "{employer_name}"\nЗарплата: до {salary_to} {currency}\nСсылка:{url}\n')
                elif salary_to == 0:
                    print(
                        f'Вакансия: {job_title} от "{employer_name}"\nЗарплата: от {salary_from} {currency}\nСсылка:{url}\n')
                else:
                    print(
                        f'Вакансия: {job_title} от "{employer_name}"\nЗарплата: от {salary_from} до {salary_to} {currency}\nСсылка:{url}\n')

    def get_avg_salary(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG(salary_from)+AVG(salary_to)/2 as avg_salary, currency FROM vacancy
                GROUP BY currency
                """
            )
            result = cur.fetchall()
            for row in result:
                avg_salary, currency = row
                print(f'Средняя зарплата по вакансиям в {currency}: {round(avg_salary, 2)}')

    def get_vacancies_with_higher_salary(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT vacancy.job_title, vacancy.salary_from, vacancy.salary_to, vacancy.currency, vacancy.description, vacancy.area, vacancy.url
                FROM vacancy
                JOIN employers ON vacancy.id_employer = employers.id_company
                GROUP BY vacancy.job_title, vacancy.salary_from, vacancy.salary_to, vacancy.currency, vacancy.description, vacancy.area, vacancy.url
                HAVING AVG(vacancy.salary_from)+AVG(salary_to)/2 > (
                SELECT AVG(salary_from)+AVG(salary_to)/2
                FROM vacancy)
                """
            )
            result = cur.fetchall()
            for row in result:
                job_title, salary_from, salary_to, currency, description, area, url = row
                if salary_from == 0 and salary_to == 0:
                    print(
                        f'Вакансия: {job_title}\nЗарплата не указана\nОписание вакансии: {description}\nГород: {area}\nСсылка:{url}\n')
                elif salary_from == 0:
                    print(
                        f'Вакансия: {job_title}\nЗарплата: до {salary_to} {currency}\nОписание вакансии: {description}\nГород: {area}\nСсылка:{url}\n')
                elif salary_to == 0:
                    print(
                        f'Вакансия: {job_title}\nЗарплата: от {salary_from} {currency}\nОписание вакансии: {description}\nГород: {area}\nСсылка:{url}\n')
                else:
                    print(
                        f'Вакансия: {job_title}\nЗарплата: от {salary_from} до {salary_to} {currency}\nОписание вакансии: {description}\nГород: {area}\nСсылка:{url}\n')

    def get_vacancies_with_keyword(self, keyword):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT vacancy.job_title, vacancy.salary_from, vacancy.salary_to, 
                vacancy.currency, vacancy.description, vacancy.area, vacancy.url
                FROM vacancy
                JOIN employers ON vacancy.id_employer = employers.id_company
                WHERE LOWER(vacancy.job_title) LIKE %s
                """,
                ('%' + keyword + '%',)
            )
            result = cur.fetchall()
            for row in result:
                job_title, salary_from, salary_to, currency, description, area, url = row
                if salary_from == 0 and salary_to == 0:
                    print(
                        f'Вакансия: {job_title}\nЗарплата не указана\nОписание вакансии: {description}\nГород: {area}\nСсылка:{url}\n')
                elif salary_from == 0:
                    print(
                        f'Вакансия: {job_title}\nЗарплата: до {salary_to} {currency}\nОписание вакансии: {description}\nГород: {area}\nСсылка:{url}\n')
                elif salary_to == 0:
                    print(
                        f'Вакансия: {job_title}\nЗарплата: от {salary_from} {currency}\nОписание вакансии: {description}\nГород: {area}\nСсылка:{url}\n')
                else:
                    print(
                        f'Вакансия: {job_title}\nЗарплата: от {salary_from} до {salary_to} {currency}\nОписание вакансии: {description}\nГород: {area}\nСсылка:{url}\n')
