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


class AdvertisementBanner(models.Model):
    name = models.CharField(max_length=200)
    image = models.FileField(upload_to="advertisement_banners/")
    link = models.URLField(help_text="Company URL opened when users click this banner")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return self.name


class SubscribeForm(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=50)
    organisation = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    telephone = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50)
    email = models.EmailField(max_length=256)
    password = models.CharField(max_length=50)
    subscription_type = models.CharField(max_length=50, choices=[("0", "No Thanks"), ("1 Year", "1 Year"), ("2 Years", "2 Years")])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


class ContactForm(models.Model):
    query_type = models.CharField(max_length=100, choices=[("Feedback / Suggestions", "Feedback / Suggestions"), ("Sales", "Sales"), ("Customer Care", "Customer Care")])
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=256)
    organisation = models.CharField(max_length=100)
    subject = models.CharField(max_length=250)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.query_type}"