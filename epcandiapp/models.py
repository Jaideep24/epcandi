from django.db import models

# Create your models here.
class News(models.Model):
    heading=models.CharField(max_length=200)
    category=models.CharField(max_length=200, choices=[("A","Aviation"),("C","Cement"),("I","Infrastructure"),("IT","IT and Telecom"),("O","Oil and Gas"),("P","Power"),("R","Real Estate")])
    news=models.TextField()
class Articles(models.Model):
    heading=models.CharField(max_length=200)
    article=models.TextField()
class Interview(models.Model):
    heading=models.CharField(max_length=200)
    Interview=models.TextField()
class Equipment_News(models.Model):
    heading=models.CharField(max_length=200)
    equipment_news=models.TextField()
class Events(models.Model):
    name=models.CharField(max_length=200)
    start_date=models.DateField()
    end_date=models.DateField()
    venue=models.CharField(max_length=200)
    timings=models.CharField(max_length=200)
    contact_details=models.CharField(max_length=200)
    website=models.URLField()