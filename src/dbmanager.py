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

