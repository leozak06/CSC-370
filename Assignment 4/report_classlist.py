# report_classlist.py
# CSC 370 - Spring 2018 - Starter code for Assignment 4
#
# The code below generates a mockup of the output of report_classlist.py
# as specified in the assignment. You can copy and paste the functions in this
# program into your solution to ensure the correct formatting.
#
# B. Bird - 02/26/2018

import psycopg2, sys

def print_header(course_code, course_name, term, instructor_name):
	print("Class list for %s (%s)"%(str(course_code), str(course_name)) )
	print("  Term %s"%(str(term), ) )
	print("  Instructor: %s"%(str(instructor_name), ) )
	
def print_row(student_id, student_name, grade):
	if grade is not None:
		print("%10s %-25s   GRADE: %s"%(str(student_id), str(student_name), str(grade)) )
	else:
		print("%10s %-25s"%(str(student_id), str(student_name),) )

def print_footer(total_enrolled, max_capacity):
	print("%s/%s students enrolled"%(str(total_enrolled),str(max_capacity)) )
	
if len(sys.argv) < 3:
	print('Usage: %s <course code> <term>'%sys.argv[0], file=sys.stderr)
	sys.exit(0)
	
course_code, term = sys.argv[1:3]

psql_user='leozak' #username
psql_db='leozak' #personal DB name
psql_password= 'V00840048' #password
psql_server='studdb2.csc.uvic.ca'
psql_port=5432

conn=psycopg2.connect(dbname=psql_db,user=psql_user, password=psql_password, host=psql_server, port=psql_port)

cursor=conn.cursor()

try:
	cursor.execute("""select student_id, student_name, course_code, course_name, term_code,final_grade, instructor_name, maximum_capacity, total_enrolled
		from course_offering
		natural join students
		natural join grades
		natural join (
		select term_code, course_code, count(student_id) as total_enrolled
		from enrollment
		group by course_code, term_code
		union
		select term_code, course_code, 0 as count
		from
		(select term_code, course_code from course_offering
		except
		select term_code, course_code from enrollment) as X) as Y
		where term_code= %s
		and course_code=%s
		union
		select student_id, student_name, course_code, course_name, term_code,final_grade, instructor_name, maximum_capacity, total_enrolled
		from course_offering
		natural join students
		natural join (
		select term_code, course_code, count(student_id) as total_enrolled
		from enrollment
		group by course_code, term_code
		union
		select term_code, course_code, 0 as count
		from
		(select term_code, course_code from course_offering
		except
		select term_code, course_code from enrollment) as X) as Y
		natural left outer join grades
		where final_grade is null
		and term_code=%s
		and course_code=%s
		order by student_id;""",(term,course_code,term,course_code))

except psycopg2.ProgrammingError as err: 
			#ProgrammingError is thrown when the database error is related to the format of the query (e.g. syntax error)
			print("Caught a ProgrammingError:",file=sys.stderr)
			print(err,file=sys.stderr)
			conn.rollback()
except psycopg2.IntegrityError as err: 
			#IntegrityError occurs when a constraint (primary key, foreign key, check constraint or trigger constraint) is violated.
			print("Caught an IntegrityError:",file=sys.stderr)
			print(err,file=sys.stderr)
			conn.rollback()
except psycopg2.InternalError as err:  
			#InternalError generally represents a legitimate connection error, but may occur in conjunction with user defined functions.
			#In particular, InternalError occurs if you attempt to continue using a cursor object after the transaction has been aborted.
			#(To reset the connection, run conn.rollback() and conn.reset(), then make a new cursor)
			print("Caught an IntegrityError:",file=sys.stderr)
			print(err,file=sys.stderr)
			conn.rollback()


row = cursor.fetchone()
print_header(row[2], row[3], row[4], row[6])
total_enrollment=row[8]
maximum_capacity=row[7]
rows_found = 0

while True:
	if row is None:
		break
	rows_found += 1
	print_row(row[0],row[1],row[5])
	row = cursor.fetchone()
	
print_footer(total_enrollment, maximum_capacity)


cursor.close()
conn.close()


'''
# Mockup: Print a class list for CSC 370
course_code = 'CSC 370'
course_name = 'Database Systems'
course_term = 201801
instructor_name = 'Bill Bird'
print_header(course_code, course_name, course_term, instructor_name)

#Print records for a few students
print_row('V00123456', 'Rebecca Raspberry', 81)
print_row('V00123457', 'Alissa Aubergine', 90)
print_row('V00123458', 'Neal Naranja', 83)

#Print the last line (enrollment/max_capacity)
print_footer(3,150)

'''