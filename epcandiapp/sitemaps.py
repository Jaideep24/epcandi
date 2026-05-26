from django.http import HttpResponse
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import (
    AboutPage,
    DisclaimerPage,
    EquipmentNews,
    Events,
    Focus,
    GuestArticle,
    Interview,
    News,
    PrivacyPage,
    ShoppingCart,
    SquareFoot,
)


class RouteSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7
    route_names = []

    def items(self):
        return self.route_names

    def location(self, item):
        return reverse(item)


class PublicContentSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    model = None
    url_name = ""

    def items(self):
        return self.model.objects.all().order_by("-id")

    def location(self, item):
        return reverse(self.url_name, args=[item.pk])


class PublishedPageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6
    model = None
    url_name = ""

    def items(self):
        return self.model.objects.filter(is_published=True).order_by("-updated_at", 
"-id")[:1]

    def location(self, item):
        return reverse(self.url_name)

    def lastmod(self, item):
        return item.updated_at


class HomeSitemap(RouteSitemap):
    route_names = ["home"]


class SectionPageSitemap(RouteSitemap):
    route_names = ["equipment", "focus", "guest_article", "square_foot", "events", "contact", "subscribe"]


class NewsSitemap(PublicContentSitemap):
    model = News
    url_name = "news-detail"


class FocusSitemap(PublicContentSitemap):
    model = Focus
    url_name = "focus-detail"


class GuestArticleSitemap(PublicContentSitemap):
    model = GuestArticle
    url_name = "guest-article-detail"


class InterviewSitemap(PublicContentSitemap):
    model = Interview
    url_name = "interview-detail"


class EquipmentSitemap(PublicContentSitemap):
    model = EquipmentNews
    url_name = "equipment-detail"


class EventsSitemap(PublicContentSitemap):
    model = Events
    url_name = "event-detail"


class ShoppingCartSitemap(PublicContentSitemap):
    model = ShoppingCart
    url_name = "shopping-cart-detail"


class SquareFootSitemap(PublicContentSitemap):
    model = SquareFoot
    url_name = "square-foot-detail"


class AboutPageSitemap(PublishedPageSitemap):
    model = AboutPage
    url_name = "about"


class DisclaimerPageSitemap(PublishedPageSitemap):
    model = DisclaimerPage
    url_name = "disclaimer"


class PrivacyPageSitemap(PublishedPageSitemap):
    model = PrivacyPage
    url_name = "privacy"


sitemaps = {
    "home": HomeSitemap,
    "sections": SectionPageSitemap,
    "news": NewsSitemap,
    "focus_items": FocusSitemap,
    "guest_articles": GuestArticleSitemap,
    "interviews": InterviewSitemap,
    "equipment_news": EquipmentSitemap,
    "events": EventsSitemap,
    "shopping_cart": ShoppingCartSitemap,
    "square_foot": SquareFootSitemap,
    "about": AboutPageSitemap,
    "disclaimer": DisclaimerPageSitemap,
    "privacy": PrivacyPageSitemap,
}


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse("sitemap"))
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /analytics/",
        "Disallow: /api/",
        "Disallow: /track/",
        f"Sitemap: {sitemap_url}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")