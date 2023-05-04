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

### sql запрос на выгрузку всех вакансий и ссылка на вакансию
SELECT employers.employer_name, vacancy.job_title, vacancy.salary_from, vacancy.salary_to,
vacancy.currency, vacancy.url
FROM vacancy JOIN employers ON vacancy.id_employer = employers.id_company

### sql запрос на получение средней зарплаты по вакансиям в определённой валюте
SELECT AVG(salary_from)+AVG(salary_to)/2 as avg_salary, currency FROM vacancy
GROUP BY currency

### sql запрос на получение вакансий у которых зарплата выше средней по таблице
SELECT vacancy.job_title, vacancy.salary_from, vacancy.salary_to, vacancy.currency, vacancy.description, vacancy.area, vacancy.url
FROM vacancy
JOIN employers ON vacancy.id_employer = employers.id_company
GROUP BY vacancy.job_title, vacancy.salary_from, vacancy.salary_to, vacancy.currency, vacancy.description, vacancy.area, vacancy.url
HAVING AVG(vacancy.salary_from)+AVG(salary_to)/2 > (
SELECT AVG(salary_from)+AVG(salary_to)/2
FROM vacancy)
