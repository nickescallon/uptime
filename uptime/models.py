from django.db import models
from django.db.models import Avg, Count
from datetime import datetime, date, timedelta
import StringIO
import csv
import HTMLParser
# Create your models here.

class Product(models.Model):
	name = models.CharField(max_length=200)
	url = models.CharField(max_length=200)
	enabled = models.BooleanField(default=False)
	
	def avg_response_time(self):
	#returns the average response time for the current month of the current year
		date = datetime.now()
		year = date.year
		month = date.month
		results = Poll.objects.filter(product__name = self.name).filter(timestamp__month = month).filter(timestamp__year = year).aggregate(Avg('rsp_time'))
		return int(results['rsp_time__avg'])
		
	def availability(self):
	#returns the availability for the current month of the current year
		date = datetime.now()
		year = date.year
		month = date.month
		total_successes = Poll.objects.filter(product__name = self.name).filter(timestamp__month = month).filter(timestamp__year = year).filter(success = 1).aggregate(Count('success'))
		total_failures = Poll.objects.filter(product__name = self.name).filter(timestamp__month = month).filter(timestamp__year = year).filter(failure = 1).aggregate(Count('failure'))
		a = float(total_failures['failure__count'])
		b = float(total_successes['success__count'])
		if  total_failures['failure__count'] != 0:
			availability = 100 * (1 - (a / b))
			if availability % 1 == 0:
				return int(availability)
			else:
				return '%.4f' % availability
		else:
			return 100
	
	def change(self):
		today = date.today()
		day_reset = date(day = 1, month = today.month, year = today.year)
		last_month_date = day_reset - timedelta(days = 1)
		month = last_month_date.month
		year = last_month_date.year
		current_avail = float(self.availability())
		try:
			last_avail_results = Monthly_Averages.objects.filter(product__name = self.name).filter(date__month = month).filter(date__year = year)
			last_avail = float(last_avail_results[0].availability)
			change = current_avail - last_avail	
			if change > 0:
				return "+ %.4f" % change
			elif change == 0:
				return int(0)
			elif change < 0:
				return str(change)
		except:
			return 0
			
	def is_it_up(self):
	#returns True if most recent Poll resulted in a Success = 1 or False if most recent Poll resulted in failure = 1
		results = Poll.objects.filter(product__name = self.name).order_by('-timestamp')[0]
		if results.success == 1:
			return True
		else:
			return False
	
	def get_projects(self):
	#returns an array of projects 
		results = Project.objects.filter(product__name = self.name).order_by('-id')
		return results
		
	def get_deployments(self):
	#returns an array of deployments 
		results = Deployment.objects.filter(product__name = self.name).order_by('-date')
		return results
	
	def getFailures(self):
	#returns an array of polls where failure == True
		results = Poll.objects.filter(product__name = self.name).filter(failure = True).order_by('-timestamp')
		return results
	
	def get_hist_availability_table(self):
	#returns an array of averages in reverse order for tables (only last 5 entries)
		results = Monthly_Averages.objects.filter(product__name = self.name).order_by('-date')[:5]
		return results
	
	def get_hist_availability_graph(self):
	#returns an array of averages in in order for graphs
		results = Monthly_Averages.objects.filter(product__name = self.name).order_by('date')
		return results
		
	def get_cur_availability_graph(self, n):
	#returns an array of averages in in order for graphs
		results = Poll.objects.filter(product__name = self.name).order_by('-timestamp')[:n]
		return results
	
	def __unicode__(self):
		return self.name

		
		
class Poll (models.Model):
	product = models.ForeignKey(Product)
	success = models.BooleanField(default=False)
	failure = models.BooleanField(default=False)
	rsp_time = models.IntegerField(null=True)
	rsp_code = models.IntegerField(null=True)
	timestamp = models.DateField(auto_now_add=True)
	
	def __unicode__(self):
		return self.product.name
	
	
	
class Monthly_Averages (models.Model):
	class Meta:
		verbose_name_plural = "Monthly Averages"

	product = models.ForeignKey(Product)
	date = models.DateField(null=False)
	availability = models.DecimalField(max_digits=7, decimal_places=4, null=False)
	avg_rsp_time = models.IntegerField(null=False)
	
	def __unicode__(self):
		return self.product.name
	

class Deployment (models.Model):
	STATUS_CHOICES = (
		('Pending', 'pending'),
		('Completed', 'completed'),
	)
	product = models.ForeignKey(Product)
	version = models.CharField(max_length=20)
	date = models.DateField(null=False)
	status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='pending')
	
	def __unicode__(self):
		return self.product.name
	
	
class Project (models.Model):
	STATUS_CHOICES = (
		('In Progress', 'in progress'),
		('Completed', 'completed'),
	)
	proj_name = models.CharField(max_length=50)
	product = models.ForeignKey(Product)
	status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='in progress')
	updates = models.TextField()
	
	def __unicode__(self):
		return self.product.name
		
		
