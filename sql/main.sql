CREATE DATABASE hranalysis;
USE hranalysis;


CREATE TABLE hr_employee (
    satisfaction_level FLOAT,
    last_evaluation FLOAT,
    number_project INT,
    average_monthly_hours INT,
    time_spend_company INT,
    Work_accident TINYINT,
    employee_left TINYINT,
    promotion_last_5years TINYINT,
    department VARCHAR(50),
    salary VARCHAR(20)
);



SELECT *
FROM hr_employee
WHERE satisfaction_level IS NULL;


UPDATE hr_employee
SET satisfaction_level = (
    SELECT median_val
    FROM (
        SELECT AVG(satisfaction_level) AS median_val
        FROM hr_employee
        WHERE satisfaction_level IS NOT NULL
    ) t
)
WHERE satisfaction_level IS NULL; 


SELECT *
FROM hr_employee
WHERE last_evaluation > 1;

UPDATE hr_employee
SET last_evaluation =(
    SELECT AVG(last_evaluation)
    FROM (
        SELECT last_evaluation FROM 
        hr_employee WHERE
        last_evaluation between 0 and 1 
    ) t   
)
WHERE last_evaluation > 1;

SELECT * FROM hr_employee
WHERE salary not in ('low','medium','high');

UPDATE hr_employee 
SET salary ='medium'
WHERE salary='nme';

SELECT * FROM hr_employee
WHERE promotion_last_5years>1;


SELECT *,
COUNT(*) as cnt
FROM hr_employee
GROUP BY satisfaction_level,last_evaluation,number_project,
average_monthly_hours,time_spend_company,
Work_accident,employee_left,
promotion_last_5years,department,salary
HAVING COUNT(*) > 1;


SELECT DISTINCT department
FROM hr_employee;


SELECT MIN(satisfaction_level), MAX(satisfaction_level)
FROM hr_employee;

SELECT MIN(last_evaluation), MAX(last_evaluation)
FROM hr_employee;

SELECT *
FROM hr_employee
WHERE number_project < 0
OR average_monthly_hours < 0
OR time_spend_company < 0;


SELECT * FROM hr_employee;
