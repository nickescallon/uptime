#THIS JOB IS INTENDED TO BE RUN ONCE PER MONTH. IT WILL ITERATE THROUGH ALL PRODUCTS
#AND CHECK TO SEE IF THEY HAVE ENTRIES FOR THE PREVIOUS MONTH IN THE uptime_monthly_averages TABLE.
#IF THERE IS NO ENTRY, IT WILL CALCULATE THE AVAILABILITY (failures/successes) AND AVERAGE RESPONSE TIME
#FOR THE PREVIOUS MONTH, AND MAKE AN ENTRY INTO THE DB. THE PURPOSE OF THIS TABLE IS TO KEEP A HISTORICAL
#RECORD OF THIS INFORMATION

import urllib2
import MySQLdb as mdb
from datetime import date, timedelta
from time import time

#calculates the availability for the product_id for the last month
def calc_monthly_uptime(product_id):
	today = date.today()
	day_reset = date(day = 1, month = today.month, year = today.year)
	end_of_last_month = day_reset - timedelta(days = 1)
	begin_of_last_month = date(day = 1, month = end_of_last_month.month, year = end_of_last_month.year)
	con = mdb.connect('localhost', 'dev_user', 'dev_user', 'dashboard');
	with con:
		cur = con.cursor()
		#gets the total number of successes for the product in the last month
		get_success = cur.execute("SELECT COUNT(*) FROM uptime_poll WHERE product_id = %s AND success = 1 AND timestamp BETWEEN %s AND %s", (product_id, begin_of_last_month, end_of_last_month))
		success_results = cur.fetchone()
		total_successes = float(success_results[0])
		#gets the total number of failures for the product in the last month
		get_failure = cur.execute("SELECT COUNT(*) FROM uptime_poll WHERE product_id = %s AND failure = 1 AND timestamp BETWEEN %s AND %s", (product_id, begin_of_last_month, end_of_last_month))
		failure_results = cur.fetchone()
		total_failures = float(failure_results[0])
	if  total_failures != 0:
		availability = 100 * (1 - (total_failures / total_successes))
		if availability % 1 == 0:
			return int(availability)
		else:
			return '%.4f' % availability
	else:
		return 100
		
#calculates the average response time for the product_id for the last month
def calc_monthly_rsp_time(product_id):
	today = date.today()
	day_reset = date(day = 1, month = today.month, year = today.year)
	end_of_last_month = day_reset - timedelta(days = 1)
	begin_of_last_month = date(day = 1, month = end_of_last_month.month, year = end_of_last_month.year)
	con = mdb.connect('localhost', 'dev_user', 'dev_user', 'dashboard');
	with con:
		cur = con.cursor()
		#gets the average response time for the product in the last month
		get_avg_rspt = cur.execute("SELECT AVG(rsp_time) FROM uptime_poll WHERE product_id = %s AND timestamp BETWEEN %s AND %s", (product_id, begin_of_last_month, end_of_last_month))
		avg_rspt_results = cur.fetchone()
		avg_rspt = float(avg_rspt_results[0])
	return int(avg_rspt)
		
		
		
#checks to see if there is an entry for product for the previous month of the current year
def check_if_exists(product_id):
	today = date.today()
	day_reset = date(day = 1, month = today.month, year = today.year)
	end_of_last_month = day_reset - timedelta(days = 1)
	begin_of_last_month = date(day = 1, month = end_of_last_month.month, year = end_of_last_month.year)
	con = mdb.connect('localhost', 'dev_user', 'dev_user', 'dashboard');
	with con:
		cur = con.cursor()
		exists = cur.execute("SELECT * FROM uptime_monthly_averages WHERE product_id = %s AND date BETWEEN %s AND %s", (product_id, begin_of_last_month, end_of_last_month))
	if exists:
		return True
	else:
		return False
		
def dblogavg(pid, uptime, response_time):
	today = date.today()
	day_reset = date(day = 1, month = today.month, year = today.year)
	end_of_last_month = day_reset - timedelta(days = 1)
	begin_of_last_month = date(day = 1, month = end_of_last_month.month, year = end_of_last_month.year)
	con = mdb.connect('localhost', 'dev_user', 'dev_user', 'dashboard');
	with con:
		cur = con.cursor()
		cur.execute("INSERT INTO uptime_monthly_averages VALUES( NULL, %s, %s, %s, %s)", (pid, begin_of_last_month, uptime, response_time))
		
	print " avg logged in DB"
		

#Returns a queryset with all records from the uptime_product table
def get_product_list():
	con = mdb.connect('localhost', 'dev_user', 'dev_user', 'dashboard');
	with con:
		cur = con.cursor()
		results = cur.execute("SELECT * FROM uptime_product")
		product_list = cur.fetchall()
	return product_list
	


prods = get_product_list()
for p in prods:
	pid = p[0]
	print pid
	if not check_if_exists(pid):
		uptime =  calc_monthly_uptime(pid)
		response_time = calc_monthly_rsp_time(pid)
		print uptime
		print response_time
		dblogavg(pid, uptime, response_time)
	else:
		print "avg data already exists in DB for this last month"

print "program complete"
		
		
