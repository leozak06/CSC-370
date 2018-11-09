-- CSC 370 - Spring 2018
-- Assignment 3: Queries for Question 2 (ferries)
-- Name: Leoza Kabir	
-- Student ID: V00840048

-- Place your query for each sub-question in the appropriate position
-- below. Do not modify or remove the '-- Question 2x --' header before
-- each question.


-- Question 2a --
with
vessel_pairs as (
select V1.vessel_name as vessel1, V2.vessel_name as vessel2
from sailings as V1
cross join sailings as V2
where V1.scheduled_departure = V2.scheduled_departure
and V1.route_number = V2.route_number )
select vessel1, vessel2, count(vessel2) as pair_count
from vessel_pairs
where vessel1 < vessel2
group by vessel1, vessel2;

-- Question 2b --
select route_number, nominal_duration, avg_duration
from routes
natural join (
select route_number,
	avg((extract(epoch from arrival)-extract(epoch from scheduled_departure))/60) as avg_duration
	from sailings
	group by route_number) as X;
			

-- Question 2c --
with month_crossing_time as (select route_number, 
(extract(epoch from arrival)-extract(epoch from scheduled_departure))/60 as crossing_time,
extract(month from scheduled_departure) as month_saling, extract(day from scheduled_departure) as day_saling
from sailings
where route_number=1)
select month_saling, count(day_saling) as count
from (
select route_number, month_saling, day_saling
from month_crossing_time
except
select route_number, month_saling, day_saling
from month_crossing_time
natural join routes
where crossing_time>=nominal_duration+5) as L
group by month_saling
order by month_saling;

-- Question 2d --

with total as (select vessel_name, count(actual_departure) as total_sailings
from sailings
group by vessel_name
order by vessel_name),

month_crossing_time as (select vessel_name, route_number, 
(extract(epoch from arrival)-extract(epoch from scheduled_departure))/60 as crossing_time,
extract(month from scheduled_departure) as month_saling, extract(day from scheduled_departure) as day_saling
from sailings),

late as (select vessel_name, count(*) as late_sailing  
from (
select vessel_name
from month_crossing_time
natural join routes
where crossing_time>=nominal_duration+5) as L
group by vessel_name
union
select vessel_name, 0 as late_sailing
from (
select vessel_name
from month_crossing_time
group by vessel_name
except
select vessel_name as late_sailing
from month_crossing_time
natural join routes
where crossing_time>=nominal_duration+5
group by vessel_name) as Y
order by vessel_name)

select distinct vessel_name, total_sailings, late_sailing, late_sailing::decimal/total_sailings as late_fraction
from total
natural join late;

-- Question 2e --

-- Question 2f --

-- Question 2g --
select vessel_name, count(*) as made_up_sailing
from (
select vessel_name,scheduled_departure, actual_departure, arrival
from (
select vessel_name, route_number, extract(epoch from actual_departure)/60 as actual_departure,
	extract(epoch from scheduled_departure)/60as scheduled_departure, 
	extract(epoch from arrival)/60as arrival
from sailings) as L
natural join routes
where actual_departure >= scheduled_departure + 15
and arrival<= scheduled_departure+nominal_duration+5) as K
group by vessel_name; 




