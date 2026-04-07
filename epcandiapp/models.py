from django.db import models

# Create your models here.
class News(models.Model):
    heading=models.CharField(max_length=200)
    category=models.CharField(max_length=200, choices=[("A","Aviation"),("C","Cement"),("I","Infrastructure"),("IT","IT and Telecom"),("O","Oil and Gas"),("P","Power"),("R","Real Estate")])
    top_news = models.BooleanField(default=False, help_text="Display this item first on the news landing page")
    news=models.TextField()

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return self.heading


class Articles(models.Model):
    heading=models.CharField(max_length=200)
    article=models.TextField()

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.heading


class GuestArticle(models.Model):
    heading=models.CharField(max_length=200)
    article=models.TextField()

    class Meta:
        verbose_name = "Guest Article"
        verbose_name_plural = "Guest Articles"

    def __str__(self):
        return self.heading


class Interview(models.Model):
    heading=models.CharField(max_length=200)
    Interview=models.TextField()

    def __str__(self):
        return self.heading

    class Meta:
        verbose_name = "Interview"
        verbose_name_plural = "Interviews"


class Equipment_News(models.Model):
    heading=models.CharField(max_length=200)
    equipment_news=models.TextField()

    def __str__(self):
        return self.heading

    class Meta:
        verbose_name = "Equipment News"
        verbose_name_plural = "Equipment News"


class Events(models.Model):
    name=models.CharField(max_length=200)
    start_date=models.DateField()
    end_date=models.DateField()
    venue=models.CharField(max_length=200)
    timings=models.CharField(max_length=200)
    contact_details=models.CharField(max_length=200)
    website=models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"


class PageContentBase(models.Model):
    title = models.CharField(max_length=255)
    heading = models.CharField(max_length=255)
    content = models.TextField()
    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-updated_at", "-id"]

    def __str__(self):
        return self.title


class AboutPage(PageContentBase):
    class Meta(PageContentBase.Meta):
        verbose_name = "About"
        verbose_name_plural = "About"


class DisclaimerPage(PageContentBase):
    class Meta(PageContentBase.Meta):
        verbose_name = "Disclaimer"
        verbose_name_plural = "Disclaimer"


class PrivacyPage(PageContentBase):
    class Meta(PageContentBase.Meta):
        verbose_name = "Privacy"
        verbose_name_plural = "Privacy"


class ShoppingCartPage(PageContentBase):
    class Meta(PageContentBase.Meta):
        verbose_name = "Shopping Cart"
        verbose_name_plural = "Shopping Cart"


class AdvertisementBanner(models.Model):
    name = models.CharField(max_length=200)
    image = models.FileField(upload_to="advertisement_banners/")
    link = models.URLField(help_text="Company URL opened when users click this banner")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "Advertisement Banner"
        verbose_name_plural = "Advertisement Banners"

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
        verbose_name = "Subscribe Form"
        verbose_name_plural = "Subscribe Forms"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


class ContactForm(models.Model):
    query_type = models.CharField(max_length=100, choices=[("Feedback / Suggestions", "Feedback / Suggestions"), ("Sales", "Sales"), ("Customer Care", "Customer Care"), ("Advertise", "Advertise")])
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=256)
    organisation = models.CharField(max_length=100)
    subject = models.CharField(max_length=250)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Form"
        verbose_name_plural = "Contact Forms"

    def __str__(self):
        return f"{self.name} - {self.query_type}"