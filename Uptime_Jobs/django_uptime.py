import urllib2
import MySQLdb as mdb
from datetime import datetime
from time import time

#Checks to see if the HTTP response code of "url"
#is 200 or 302. If so, the url is UP and the function
#returns True. Otherwise it returns False
def issiteup(url):
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)')]
		response = opener.open(url)
		status = response.code
		if (status != 200) and (status != 302):
			print url + " bad response " + str(status)
			return False
		else:
			return True
	except:
		print url + " timed out"
		return False

		
def response_time(url):
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)')]
		start = time()
		request = opener.open(url, None, 5.0)
		end = time()
		response_time = (end - start)
		response_time_int = int(response_time * 1000)
		return str(response_time_int)
	except:
		return "was not available"

#Inserts data into the "failures" table of the dashboard DB
def dblogfailure(pid):
	con = mdb.connect('localhost', 'dev_user', 'dev_user', 'dashboard');
	with con:
		cur = con.cursor()
		cur.execute("INSERT INTO uptime_poll VALUES( NULL, %s, %s, %s, NULL, NULL, NULL)", (pid, False, True))
		
	print "failure logged in DB"

#Inserts data into the "response_time" table of the dashboard DB
def dblogrt(pid, rt):
	con = mdb.connect('localhost', 'dev_user', 'dev_user', 'dashboard');
	with con:
		cur = con.cursor()
		cur.execute("INSERT INTO uptime_poll VALUES( NULL, %s, %s, %s, %s, %s, NULL)", (pid, True, False, rt, 200))
		
	print "response time logged in DB"

#Returns a queryset with all records from the uptime_product table
def get_product_list():
	con = mdb.connect('localhost', 'dev_user', 'dev_user', 'dashboard');
	with con:
		cur = con.cursor()
		results = cur.execute("SELECT * FROM uptime_product")
		product_list = cur.fetchall()
	return product_list
	

#Iterates though all products, checks if
#they are up, and logs either a response time value or a
#failure value in the DB

prods = get_product_list()
for p in prods:
	pid = p[0]
	print pid
	url = p[2]
	print url
	if issiteup(url):
		print p[1] + " is up"
		rt = response_time(url)
		print str(rt)
		dblogrt(pid, rt)
	else:
		dblogfailure(pid)


print "program complete"
		
		
