### создание таблицы с вакансиями
CREATE TABLE vacancy (
  id VARCHAR(50) PRIMARY KEY,
  job_title VARCHAR(100) NOT NULL,
  salary_from INTEGER NOT NULL,
  salary_to INTEGER NOT NULL,
  currency VARCHAR(10) NOT NULL,
  description TEXT,
  area VARCHAR(100) NOT NULL,
  id_employer VARCHAR(50),
  employer VARCHAR(100) NOT NULL,
  url VARCHAR(200) NOT NULL,
  date TIMESTAMP NOT NULL
);
### создание таблицы с компаниями
CREATE TABLE employers (
id_company VARCHAR(50) PRIMARY KEY,
employer_name VARCHAR(100),
description TEXT,
site TEXT
);

### запрос sql на выгрузку количества вакансий у компании
SELECT employers.employer_name, COUNT(vacancy.id) as count_vacancies
FROM vacancy JOIN employers ON vacancy.id_employer = employers.id_company
GROUP BY employers.employer_name