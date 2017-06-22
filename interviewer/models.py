from django.db import models

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=200)
    updated_date = models.DateTimeField('date updated')


class Users(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)