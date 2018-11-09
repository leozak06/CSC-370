-- CSC 370 - Spring 2018
-- Assignment 2: Queries for Question 2 (ferries)
-- Name: Leoza Kabir
-- Student ID: V00840048

-- Place your query for each sub-question in the appropriate position
-- below. Do not modify or remove the '-- Question 2x --' header before
-- each question.


-- Question 2a --
select vessel_name
from sailings
where route_number=1
group by vessel_name;

-- Question 2b --
select vessel_name, count(vessel_name) as count
from sailings
group by vessel_name;


-- Question 2c --
select vessel_name, num_routes
from 
(select vessel_name, count(distinct route_number) as num_routes
from sailings
group by vessel_name) as X
where num_routes>=2;


-- Question 2d --



-- Question 2e --