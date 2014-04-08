from django.conf.urls import patterns, url

from uptime import views

urlpatterns = patterns('',
    # ex: /uptime/
	url(r'^$', views.index, name='index'),
	# ex: /uptime/t1thin/
	url(r'^(?P<product_name>\w+)/$', views.product, name='product'),
	# ex: /uptime/t1thin/deployments/
	url(r'^(?P<product_name>\w+)/deployments/$', views.productDeployments, name='deployments'),
	# ex: /uptime/t1thin/projects/
	url(r'^(?P<product_name>\w+)/projects/$', views.productProjects, name='projects'),
	# ex: /uptime/t1thin/csv/availability/
	url(r'^(?P<product_name>\w+)/csv/availability/$', views.product_csv_avail, name='product_csv_avail'),
	# ex: /uptime/t1thin/csv/response/
	url(r'^(?P<product_name>\w+)/csv/response/$', views.product_csv_resp, name='product_csv_avg_resp'),
	# ex: /uptime/t1thin/csv/response/120/
	url(r'^(?P<product_name>\w+)/csv/response/(?P<range>\d+)/$', views.product_csv_cur_resp, name='product_csv_cur_resp'),
	# ex: /uptime/t1thin/csv/faliures/
	url(r'^(?P<product_name>\w+)/csv/failures/$', views.productFailures, name='productCSVfailures'),
)