-- CSC 370 - Spring 2018
-- Assignment 3: Queries for Question 3 (vwsn_1year)
-- Name:Leoza Kabir
-- Student ID: V00840048

-- Place your query for each sub-question in the appropriate position
-- below. Do not modify or remove the '-- Question 3x --' header before
-- each question.


-- Question 3a --
with max_temp as (
select max(temperature) as high_temp from (
select station_id, temperature
from observations) as X)
select station_id, name, high_temp as temperature, observation_time
from stations
natural join observations
natural join (select station_id, high_temp, observation_time
from max_temp
inner join observations
on max_temp.high_temp=observations.temperature) as Y
where stations.id=observations.station_id;


-- Question 3b --
with list_id as (select station_id, max(temperature) as max_temperature
from observations
where station_id between 1 and 10
group by station_id)
select station_id, name, round(cast(max_temperature as numeric),1)as max_temperature, observation_time
from stations
natural join observations
natural join list_id
where max_temperature=temperature
and stations.id=observations.station_id
order by station_id;


-- Question 3c --
select station_id, name
from observations
natural join stations
where observations.station_id=stations.id
except
select station_id, name
from observations
natural join stations
where extract(month from observation_time)=6
and extract(year from observation_time)=2017
and observations.station_id=stations.id
order by station_id;

-- Question 3d --
with day_avg as (select year, month, day, avg_temp
from (
select extract(year from observation_time)as year,
extract(month from observation_time)as month, 
extract(day from observation_time) as day,
avg(temperature) as avg_temp
from observations
group by year, month, day)as X),

ranking as (select year, month, avg_temp, rank()over(partition by month order by avg_temp desc) as hottest, 
rank()over(partition by month order by avg_temp asc) as coldest
from day_avg),

hot as (select year, month, avg(avg_temp) as hottest10_average
from ranking
where hottest between 1 and 10
group by year, month),

cold as (select year, month, avg(avg_temp) as coolest10_average
from ranking
where coldest between 1 and 10
group by year, month) 

select year, month, hottest10_average, coolest10_average
from hot
natural join cold
order by year;

-- Question 3e --
