# report_enrollment.py
# CSC 370 - Spring 2018 - Starter code for Assignment 4
#
# The code below generates a mockup of the output of report_enrollment.py
# as specified in the assignment. You can copy and paste the functions in this
# program into your solution to ensure the correct formatting.
#
# B. Bird - 02/26/2018

import psycopg2, sys

def print_row(term, course_code, course_name, instructor_name, total_enrollment, maximum_capacity):
	print("%6s %10s %-35s %-25s %s/%s"%(str(term), str(course_code), str(course_name), str(instructor_name), str(total_enrollment), str(maximum_capacity)) )

psql_user='leozak' #username
psql_db='leozak' #personal DB name
psql_password= 'V00840048' #password
psql_server='studdb2.csc.uvic.ca'
psql_port=5432

conn=psycopg2.connect(dbname=psql_db,user=psql_user, password=psql_password, host=psql_server, port=psql_port)

cursor=conn.cursor()

try:
	cursor.execute(""" select term_code, course_code, course_name, instructor_name, total_enrollment, maximum_capacity
	from course_offering
	natural join (select term_code, course_code, count(student_id) as total_enrollment
				from enrollment
				group by course_code, term_code
				union
				select term_code, course_code, 0 as count
				from 
				(select term_code, course_code from course_offering
				except
				select term_code, course_code from  enrollment)as X) as Y
				order by term_code;
	
	""")

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

# Mockup: Print some data for a few made up classes

#print_row(201709, 'CSC 106', 'The Practice of Computer Science', 'Bill Bird', 203, 215)
#print_row(201709, 'CSC 110', 'Fundamentals of Programming: I', 'Jens Weber', 166, 200)
#print_row(201801, 'CSC 370', 'Database Systems', 'Bill Bird', 146, 150)


rows_found = 0
while True:
	row = cursor.fetchone()
	if row is None:
		break
	rows_found += 1
	print_row(row[0], row[1], row[2], row[3], row[4], row[5])
		#print("Row %02d: \"%s\" \"%s\""%(rows_found,row[0], row[1]) )
cursor.close()
conn.close()