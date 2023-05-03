from src.utils import creating_tables_check, connect_pg
from src.dbmanager import DBManager


if __name__ == "__main__":
    host, database, user, password = 'localhost', 'term_papers_5', 'postgres', '1346'
    creating_tables_check(host, database, user, password)
    manager = DBManager(host, database, user, password)
    manager.get_companies_and_vacancies_count()
