# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from datetime import datetime
import csv

from uptime.models import Product, Poll

def index(request):
	products = Product.objects.filter(enabled=True).order_by('name')
	context = {'products': products}
	
	return render(request, 'uptime/index.html', context)
	
def product(request, product_name):
	current_product = get_object_or_404(Product, name=product_name)
	products = Product.objects.filter(enabled=True).order_by('name')
	context = {'products' : products, 'product_name' : product_name}
	
	return render(request, 'uptime/product_page.html', context)

def product_csv_avail(request, product_name):
	current_product = get_object_or_404(Product, name=product_name)
	results = current_product.get_hist_availability_graph()
	response = HttpResponse(mimetype='text/csv')
	response['Content-Disposition'] = 'attachment; filename=%s_hist_avail.csv' % product_name
	writer = csv.writer(response)
	writer.writerow(['Date', 'Availability'])
	for items in results:
		writer.writerow([items.date,items.availability])
			
	return response

def product_csv_resp(request, product_name):
	current_product = get_object_or_404(Product, name=product_name)
	results = current_product.get_hist_availability_graph()
	response = HttpResponse(mimetype='text/csv')
	response['Content-Disposition'] = 'attachment; filename=%s_hist_rt.csv' % product_name
	writer = csv.writer(response)
	writer.writerow(['Date', 'Response Time'])
	for items in results:
		writer.writerow([items.date,items.avg_rsp_time])
			
	return response
	
def product_csv_cur_resp(request, product_name, range):
	current_product = get_object_or_404(Product, name=product_name)
	results = current_product.get_cur_availability_graph(range)
	response = HttpResponse(mimetype='text/csv')
	response['Content-Disposition'] = 'attachment; filename=%s_hist_rt.csv' % product_name
	writer = csv.writer(response)
	writer.writerow(['Time', 'Response Time'])
	for items in reversed(results):
		writer.writerow([items.timestamp,items.rsp_time])
			
	return response
	
def productFailures(request, product_name):
	current_product = get_object_or_404(Product, name=product_name)
	results = current_product.getFailures()
	response = HttpResponse(mimetype='text/csv')
	response['Content-Disposition'] = 'attachment; filename=%s_failures.csv' % product_name
	writer = csv.writer(response)
	writer.writerow(['Date'])
	for items in results:
		writer.writerow([items.timestamp])
			
	return response
	
def productDeployments(request, product_name):
	current_product = get_object_or_404(Product, name=product_name)
	products = Product.objects.filter(enabled=True).order_by('name')
	context = {'products' : products, 'product_name' : product_name}
	
	return render(request, 'uptime/deployments_page.html', context)

def productProjects(request, product_name):
	current_product = get_object_or_404(Product, name=product_name)
	products = Product.objects.filter(enabled=True).order_by('name')
	context = {'products' : products, 'product_name' : product_name}
	
	return render(request, 'uptime/projects_page.html', context)