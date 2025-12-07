
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS customers;


CREATE TABLE customers (
  customer_id SERIAL PRIMARY KEY,
  name TEXT,
  city TEXT,
  joined_date DATE
);


CREATE TABLE employees (
  employee_id SERIAL PRIMARY KEY,
  name TEXT,
  role TEXT,
  hired_date DATE
);


CREATE TABLE projects (
  project_id SERIAL PRIMARY KEY,
  project_name TEXT,
  start_date DATE,
  end_date DATE,
  manager_id INT REFERENCES employees(employee_id)
);


CREATE TABLE sales (
  sale_id SERIAL PRIMARY KEY,
  customer_id INT REFERENCES customers(customer_id),
  project_id INT REFERENCES projects(project_id),
  employee_id INT REFERENCES employees(employee_id),
  amount NUMERIC(12,2),
  sale_date DATE
);


INSERT INTO customers (name, city, joined_date) VALUES
('Asha Enterprises','Mumbai','2022-03-10'),
('Bhatia Traders','Pune','2021-11-05'),
('Crest Ltd','Nagpur','2023-01-15'),
('DigiMart','Mumbai','2020-07-22'),
('EcoGoods','Pune','2022-09-03'),
('FreshFoods','Amravati','2021-02-18'),
('GreenTech','Mumbai','2023-06-01'),
('HomePlus','Nagpur','2020-12-11'),
('InfoSysX','Pune','2019-05-09'),
('JainHouse','Amravati','2021-08-30');


INSERT INTO employees (name, role, hired_date) VALUES
('Rahul Sharma','Sales Manager','2019-04-01'),
('Priya Deshpande','Account Manager','2020-08-15'),
('Amit Gupta','Sales Executive','2021-01-10'),
('Sneha Patil','Sales Executive','2021-06-20'),
('Vikram Joshi','Project Manager','2018-12-05'),
('Neha Kulkarni','Analyst','2022-02-02');


INSERT INTO projects (project_name, start_date, end_date, manager_id) VALUES
('Alpha','2022-01-01','2022-12-31',5),
('Beta','2023-02-01','2023-10-31',5),
('Gamma','2021-06-01','2022-05-31',5),
('Delta','2023-07-01','2024-06-30',2),
('Epsilon','2020-03-01','2021-02-28',1);


INSERT INTO sales (customer_id, project_id, employee_id, amount, sale_date) VALUES
(1,1,1,120000.00,'2022-03-15'),
(2,2,3,85000.00,'2023-03-20'),
(3,2,4,45000.00,'2023-04-10'),
(4,3,1,30000.00,'2021-07-05'),
(5,4,2,150000.00,'2023-08-12'),
(6,1,3,22000.00,'2022-09-27'),
(7,4,4,98000.00,'2023-11-05'),
(8,5,1,12000.00,'2020-05-18'),
(9,2,6,75000.00,'2023-05-20'),
(10,3,2,43000.00,'2021-01-11');

