from django.db import models

# Create your models here.
SECTOR_CHOICES = [
    ("A", "Aviation"),
    ("C", "Cement"),
    ("I", "Infrastructure"),
    ("IT", "IT and Telecom"),
    ("O", "Oil and Gas"),
    ("P", "Power"),
    ("R", "Real Estate"),
]


class News(models.Model):
    heading=models.CharField(max_length=200)
    top_news = models.BooleanField(default=False, help_text="Display this item first on the news landing page")
    news=models.TextField()

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return self.heading


class Focus(models.Model):
    heading=models.CharField(max_length=200)
    category=models.CharField(max_length=200, choices=SECTOR_CHOICES, default="I")
    article=models.TextField()

    class Meta:
        verbose_name = "Focus"
        verbose_name_plural = "Focus"

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
    interview=models.TextField()

    def __str__(self):
        return self.heading

    class Meta:
        verbose_name = "Interview"
        verbose_name_plural = "Interviews"


class EquipmentNews(models.Model):
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
    banner=models.FileField(upload_to="event_banners/", blank=True, null=True)
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
    subscription_type = models.CharField(
        max_length=50,
        choices=[
            ("0", "No Thanks"),
            ("print_1y", "Print - 1 Year (12 Issues) - Rs. 1,920"),
            ("print_2y", "Print - 2 Years (24 Issues) - Rs. 3,400"),
            ("print_3y", "Print - 3 Years (36 Issues) - Rs. 5,000"),
            ("soft_1y", "Soft Copy - 1 Year (12 Issues) - Rs. 500"),
            ("soft_2y", "Soft Copy - 2 Years (24 Issues) - Rs. 1,000"),
            ("soft_3y", "Soft Copy - 3 Years (36 Issues) - Rs. 1,500"),
            ("1 Year", "Legacy - 1 Year"),
            ("2 Years", "Legacy - 2 Years"),
        ],
    )
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


class AnalyticsUser(models.Model):
    user_id = models.CharField(max_length=64, unique=True)
    anonymized_ip = models.CharField(max_length=64, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    device_type = models.CharField(max_length=20, blank=True)
    browser = models.CharField(max_length=100, blank=True)
    operating_system = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=32, blank=True)
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-last_seen"]
        verbose_name = "Analytics User"
        verbose_name_plural = "Analytics Users"

    def __str__(self):
        return self.user_id


class AnalyticsSession(models.Model):
    session_id = models.CharField(max_length=64, unique=True)
    user = models.ForeignKey(AnalyticsUser, on_delete=models.CASCADE, related_name="sessions")
    entry_page = models.CharField(max_length=400, blank=True)
    exit_page = models.CharField(max_length=400, blank=True)
    referrer = models.CharField(max_length=400, blank=True)
    source = models.CharField(max_length=120, blank=True)
    utm_source = models.CharField(max_length=120, blank=True)
    utm_medium = models.CharField(max_length=120, blank=True)
    utm_campaign = models.CharField(max_length=120, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    is_bounced = models.BooleanField(default=True)

    class Meta:
        ordering = ["-start_time"]
        verbose_name = "Analytics Session"
        verbose_name_plural = "Analytics Sessions"

    def __str__(self):
        return self.session_id


class AnalyticsEvent(models.Model):
    event_type = models.CharField(max_length=80)
    user = models.ForeignKey(AnalyticsUser, on_delete=models.CASCADE, related_name="events")
    session = models.ForeignKey(AnalyticsSession, on_delete=models.CASCADE, related_name="events")
    page_url = models.CharField(max_length=400, blank=True)
    referrer = models.CharField(max_length=400, blank=True)
    event_name = models.CharField(max_length=120, blank=True)
    metadata_json = models.TextField(default="{}", blank=True)
    duration_ms = models.PositiveIntegerField(blank=True, null=True)
    scroll_depth = models.PositiveSmallIntegerField(blank=True, null=True)
    ttfb_ms = models.PositiveIntegerField(blank=True, null=True)
    lcp_ms = models.PositiveIntegerField(blank=True, null=True)
    fid_ms = models.PositiveIntegerField(blank=True, null=True)
    cls = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Analytics Event"
        verbose_name_plural = "Analytics Events"

    def __str__(self):
        return f"{self.event_type} @ {self.timestamp:%Y-%m-%d %H:%M}"


class SquareFoot(models.Model):
    heading = models.CharField(max_length=200)
    square_foot = models.TextField()

    class Meta:
        verbose_name = "Square Foot"
        verbose_name_plural = "Square Foot"

    def __str__(self):
        return self.heading


class ShoppingCart(models.Model):
    heading = models.CharField(max_length=200)
    shopping_cart = models.TextField()

    class Meta:
        verbose_name = "Shopping Cart"
        verbose_name_plural = "Shopping Cart"

    def __str__(self):
        return self.heading