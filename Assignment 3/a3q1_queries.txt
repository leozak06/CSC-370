-- CSC 370 - Spring 2018
-- Assignment 3: Queries for Question 1 (imdb)
-- Name: Leoza Kabir
-- Student ID: V00840048

-- Place your query for each sub-question in the appropriate position
-- below. Do not modify or remove the '-- Question 1x --' header before
-- each question.


-- Question 1a --
with film_list as (
select title_id, name
from title_names
where is_primary=true),
max_rating as (
select title_id, year, rating, max(rating)over(partition by year) as highest_rating
from ratings
natural join titles
where year between 2000 and 2017
and votes >10000
and title_type='movie')
select name as primary_name, year, round(cast(rating as numeric),1) as rating, votes
from max_rating
natural join ratings
natural join titles
natural join film_list
where rating=highest_rating
order by year;

-- Question 1b --
select distinct name as primary_name, episode_count
from title_names
natural join (
select series_id as title_id, count(series_id) as episode_count
from series_episodes
group by series_id) as L
where episode_count >=6000
and is_primary=true
order by episode_count desc;

