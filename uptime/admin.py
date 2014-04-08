from django.contrib import admin
from uptime.models import Product, Poll, Monthly_Averages, Deployment, Project

admin.site.register(Poll)
admin.site.register(Monthly_Averages)
admin.site.register(Product)
admin.site.register(Deployment)
admin.site.register(Project)
