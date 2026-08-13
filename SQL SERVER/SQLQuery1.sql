-- use command; -> to select the database

USE SalesDB; 


-- SELECT < Column Names> from TABLE NAME -> to get data from the tables 

select * from Sales.Customers; -- * -> all columns 

select FirstName,LastName from Sales.Customers;

-- Where Clause - > we use it write condition 

select * from Sales.Customers
where CustomerID=2;

-- Comparision operators 
-- > < >= <= != = 

select FirstName,LastName,Score from Sales.Customers
where Score >= 500;

-- Score > 400  and country GERMANY
-- logical operators and, or , not 

select * from Sales.Customers
where score > 400 and Country = 'Germany'


-- Score > 700  or country USA
-- logical operators and, or , not 

select * from Sales.Customers
where score > 400 or Country = 'USA';

-- NOT from USA USA



select * from Sales.Customers
where country != 'USA';


-- ORDER BY operator 


select * from Sales.customers
order by SCORE;

-- ORDER BY desc


select * from Sales.customers
order by SCORE DESC;

-- example top scores
SELECT TOP 3 * FROM sales.Customers
ORDER BY SCORE DESC

-- string functions 
-- Like for strings we like keyword
-- _ -> single character 
-- % -> any number of characers
select * from Sales.Customers
where FirstName like 'Mar_';



select * from Sales.Customers;

-- CONCAT: to combine strings 
select CustomerID,FirstName,LastName,
CONCAT(FirstName,'  ',LastName)'FullName',Country, Score
From Sales.Customers;
--
-- Aggregation function
-- for calculations 
-- Examples
-- get number of people from each country 
-- Avg of scores 
-- MAX SCORE, MIN SCORE, TOTAL SCORE, AVG OF SCORE
select * from Sales.Customers;
--QUESTION1 : get count of people from each country
select Country, Count(FirstName),AVG(SCORE),MAX(SCORE),SUM(SCORE)
from Sales.Customers
Group By Country;

--


