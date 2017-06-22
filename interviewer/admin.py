from django.contrib import admin

# Register your models here.

from .models import Company, User

admin.site.register(Company)
admin.site.register(User)