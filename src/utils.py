# -*- coding: utf-8 -*-
from src.headhunter import HeadHunterAPI
from src.dbmanager import DBManager
import psycopg2


def connect_pg():
    """
        Функция для подключения к БД пользователя
    host хост базы данных
    database имя базы данных
    user имя пользователя бд
    password пароль
    """
    host = str(input('Введите хост БД:\n'))
    user = str(input('Введите имя пользователя БД:\n'))
    database = str(input('Введите имя БД:\n'))
    password = str(input('Введите пароль от БД:\n'))
    return host, database, user, password


def user_interaction():
    host, database, user, password = connect_pg()
    creating_tables(host, database, user, password)
    manager = DBManager(host, database, user, password)
    while True:
        print(
            '\nВведите команду для нужной операции в БД (для выхода з программы введите exit/выход):\n'
            '1) Вывести список всех компаний и количества их вакансий.\n2) Получение всех вакансий(с названием компании и ссылкой)\n'
            '3) Вывод информации по средней заработной плате по всем вакансиям\n4) Вывод всех вакансий у которых зарплата выше средней\n'
            '5) Поиск и вывод вакансий с ключевым словом')
        user_input = input()
        if user_input.lower() in ['exit','выход']:
            print('До скорой встречи!')
            break
        elif int(user_input) == 1:
            manager.get_companies_and_vacancies_count()
        elif int(user_input) == 2:
            manager.get_all_vacancies()
        elif int(user_input) == 3:
            manager.get_avg_salary()
        elif int(user_input) == 4:
            manager.get_vacancies_with_higher_salary()
        elif int(user_input) == 5:
            keyword_input = input('Введите слово для поиска: ')
            manager.get_vacancies_with_keyword(keyword_input)
        else:
            print('Введена неверная команда, попробуйте ещё раз')

def creating_tables(host, database, user, password):
    # host, database, user, password = 'localhost', 'term_papers_5', 'postgres', '1346'
    ### Проверка на заполненность БД
    try:
        conn = psycopg2.connect(host=host, database=database, user=user, password=password)
        cur = conn.cursor()
        # Выполняем запрос на подсчет количества записей в таблице vacancy
        cur.execute("SELECT COUNT(*) FROM vacancy")
        # Получаем результат запроса vacancy
        count_vacancy = cur.fetchone()[0]
        # Выполняем запрос на подсчет количества записей в таблице vacancy
        cur.execute("SELECT COUNT(*) FROM employers")
        # Получаем результат запроса vacancy
        count_employers = cur.fetchone()[0]
        cur.close()
        conn.close()
        if count_vacancy > 0 and count_employers > 0:
            print("Таблицы уже заполнены")
        else:
            employers_id = [1740, 78638, 3529, 733, 67611, 15478, 851604, 2686590, 80, 9418714]
            limit_vacancy = int(input('Введите количество необходимых вакансий для каждой организации:\n'))
            for employer_id in employers_id:
                hh_api = HeadHunterAPI()
                hh_vacancies, hh_employers = hh_api.get_vacancies(employer_id, limit_vacancy)
                with psycopg2.connect(
                        host=host,
                        database=database,
                        user=user,
                        password=password
                ) as conn:
                    with conn.cursor() as cur:
                        for row in hh_vacancies:
                            cur.execute(
                                "INSERT INTO vacancy (id, job_title, salary_from, salary_to, currency, description, area, id_employer, employer, url, date) VALUES (%s, %s, %s, %s, %s, %s ,%s, %s, %s, %s, %s)",
                                (row["id"], row["job_title"], row["salary_from"], row["salary_to"], row["currency"],
                                 row["description"], row["area"], row['id_employer'], row["employer"], row["url"],
                                 row["date"]))
                        for row in hh_employers:
                            cur.execute(
                                "INSERT INTO employers (id_company, employer_name, description, site) VALUES (%s, %s, %s, %s)",
                                (row["id_company"], row["employer_name"], row["description"], row["site"]))
            print('Таблицы заполнены')
    except:
        print('Неверные данные для подключения к БД')
