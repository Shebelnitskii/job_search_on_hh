CREATE TABLE vacancy (
  id VARCHAR(50) PRIMARY KEY,
  job_title VARCHAR(100) NOT NULL,
  salary_from INTEGER NOT NULL,
  salary_to INTEGER NOT NULL,
  currency VARCHAR(10) NOT NULL,
  description TEXT,
  area VARCHAR(100) NOT NULL,
  employer VARCHAR(100) NOT NULL,
  url VARCHAR(200) NOT NULL,
  date TIMESTAMP NOT NULL
);

CREATE TABLE employers (
id_vacancy INT PRIMARY KEY,
id_company INT,
employer_name VARCHAR(100),
description TEXT,
site TEXT
);