-- CSC 370 - Spring 2018
-- Assignment 2: Queries for Question 1 (imdb)
-- Name: Leoza Kabir
-- Student ID: V00840048

-- Place your query for each sub-question in the appropriate position
-- below. Do not modify or remove the '-- Question 1x --' header before
-- each question.


-- Question 1a --
select name as primary_name, year
from titles
natural join title_names
where year=1989 and length_minutes = 180 and title_type='tvSpecial';

-- Question 1b --
select name as primary_name, year, length_minutes, title_type
from titles
natural join title_names
where length_minutes >= 4320 and title_type='movie'
;

-- Question 1c --
select name as primary_name, year, length_minutes
from titles
natural join title_names
natural join
(select person_id, title_id
from people
natural join cast_crew
where name='Meryl Streep') as X
where year <= 1985 and title_type='movie';

-- Question 1d --
select name as primary_name, year, length_minutes
from titles
natural join title_names
natural join
(select title_id
from title_genres
where genre='Film-Noir') as X
where title_type='movie'
intersect
select name as primary_name, year, length_minutes
from titles
natural join title_names
natural join
(select title_id
from title_genres
where genre='Action') as Y
where title_type='movie';


-- Question 1e --
select name 
from people 
natural join
(select person_id
from cast_crew
natural join
(select title_id
from titles
natural join title_names
where name='The Big Lebowski' and title_type='movie') as X) 
as Y;

-- Question 1f --
select name
from people
natural join
(select person_id
from writers 
natural join
(select title_id
from titles
natural join title_names
where name='Die Hard' and title_type='movie') as X)as Y
union select name
from people
natural join
(select person_id
from directors 
natural join
(select title_id
from titles
natural join title_names
where name='Die Hard' and title_type='movie') as W)as Z;

-- Question 1g --
select name, length_minutes
from titles
natural join
title_names 
natural join
(select title_id,person_id 
from known_for
natural join people where name='Tom Cruise')as X
where title_type='movie'; 

-- Question 1h --
select name as primary_name, year, length_minutes
from titles
natural join title_names
natural join
(select distinct person_id, title_id
from cast_crew
natural join people where name='Tom Hanks')as X
where title_type='movie'
intersect 
select name as primary_name, year, length_minutes
from titles
natural join title_names
natural join
(select distinct person_id, title_id
from cast_crew
natural join people where name='Meryl Streep')as X
where title_type='movie'; 

-- Question 1i --
select name as primary_name, year
from titles
natural join title_genres
natural join title_names
natural join
(select title_id, person_id
from directors
natural join people where name='Steven Spielberg') as X
where genre='Thriller' and title_type='movie';