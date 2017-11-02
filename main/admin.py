from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Company)
admin.site.register(ContactDetails)
admin.site.register(Job)
admin.site.register(Question)
admin.site.register(JobQuestion)
