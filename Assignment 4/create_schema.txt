-- Leoza Kabir
-- V00840048
-- create_schema.sql
-- CSC 370- Spring 2018

--STUDENT
--only one name string may be associated with a particular student IDENTIFIED
--student IDs are unique
--every student has a student ID
--add trigger that allows a student to be added to the database more than once, with every duplicate insertion ignored as long as the name and student id match the existing record
drop table if exists students cascade;
drop function if exists student_duplication_trigger();
create table students (
	student_id varchar (10), --in the form V00xxxxxx
	student_name varchar(255), --student names must be at at most 255 characters  long, do not contain commas or semicolons or whitespcae but can contains digits
	primary key (student_id)	
);
create function student_duplication_trigger()
returns trigger as
$BODY$
begin
if (select count(*) from students
	where student_id=new.student_id)>0
then
	return null;
end if;
return new;
end
$BODY$
language plpgsql;

create trigger student_duplication
	before insert on students
	for each row
	execute procedure student_duplication_trigger();

--COURSES
drop table if exists courses cascade;
--trigger
drop function if exists courses_duplication_trigger();
create table courses(
	course_code varchar (10),
	primary key(course_code)
);
create function courses_duplication_trigger()
returns trigger as
$BODY$
begin
if (select count(*) from courses
	where course_code=new.course_code)>0
then
	--raise exception 'Student already enrolled in course';
	return null;
end if;
return new;
end
$BODY$
language plpgsql;

create trigger courses_duplication
	before insert on courses
	for each row
	execute procedure courses_duplication_trigger();

--COURSE OFFERINGS
drop table if exists course_offering cascade;
--trigger
drop function if exists offering_duplication_trigger();
create table course_offering(
	course_code varchar(10),
	course_name varchar(128) NOT NULL,
	term_code varchar(6),
	instructor_name varchar (255) NOT NULL,
	maximum_capacity int,
	check(maximum_capacity >= 0),
	primary key(course_code,term_code),
	foreign key (course_code) references courses(course_code)
);
create function offering_duplication_trigger()
returns trigger as
$BODY$
begin
if (select count(*) from course_offering
	where course_code=new.course_code
	and course_name=new.course_name
	and term_code=new.term_code
	and instructor_name = new.instructor_name
	and maximum_capacity=new.maximum_capacity)>0
then
	--raise exception 'Student already enrolled in course';
	return null;
end if;
return new;
end
$BODY$
language plpgsql;

create trigger offering_duplication
	before insert on course_offering
	for each row
	execute procedure offering_duplication_trigger();

--ENROLLMENT
drop table if exists enrollment cascade;
--trigger
drop function if exists enrollment_duplication_trigger();
create table enrollment(
	student_id varchar (10),
	student_name varchar(255),
	course_code varchar (10),
	term_code varchar (6),
	primary key(student_id, course_code,term_code),
	foreign key (course_code, term_code) references course_offering(course_code,term_code)
		on delete set null
		on update cascade
		deferrable,
	foreign key (student_id) references students
	(student_id)
		on delete restrict
		on update cascade
		deferrable
);
create function enrollment_duplication_trigger()
returns trigger as
$BODY$
begin
if (select count(*) from enrollment
	where student_id=new.student_id
	and course_code=new.course_code
	and term_code=new.term_code)>0
then
	--raise exception 'Student already enrolled in course';
	return null;
end if;
return new;
end
$BODY$
language plpgsql;

create constraint trigger enrollment_duplication
	after insert or update on enrollment
	deferrable
	for each row
	execute procedure enrollment_duplication_trigger();

--PREREQ
drop table if exists prerequisite;
--trigger
drop function if exists prerequisite_duplication_trigger();
create table prerequisite(
	course_code varchar (10),
	term_code varchar (128),
	prereq varchar(10),
	primary key (course_code, term_code, prereq),
	foreign key (course_code, term_code) references course_offering(course_code,term_code)
		on delete set null
		on update cascade
);
create function prerequisite_duplication_trigger()
returns trigger as
$BODY$
begin
if (select count(*) from prerequisite
	where course_code=new.course_code
	and term_code=new.term_code
	and prereq=new.prereq)>0
then
	--raise exception 'Student already enrolled in course';
	return null;
end if;
return new;
end
$BODY$
language plpgsql;

create trigger prerequisite_duplication
	before insert on prerequisite
	for each row
	execute procedure prerequisite_duplication_trigger();

--GRADES
drop table if exists grades;
--trigger
create table grades(
	course_code varchar (10),
	term_code varchar(6),
	student_id varchar (10),
	final_grade int
	check (final_grade >=0 and final_grade <=100),
	primary key (student_id, course_code),
	foreign key(student_id, course_code, term_code) references enrollment (student_id, course_code, term_code)
		on delete cascade
		on update set null
);


