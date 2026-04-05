from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path("", home_page, name="home"),
    path("news/", news_page, name="news"),
    path("articles/", article_page, name="articles"),
    path("articles/<int:article_id>/", article_detail_page, name="article-detail"),
    path("interview/", interview_page, name="interview"),
    path("equipment/", equipment_page, name="equipment"),
    path("events/", events_page, name="events"),
    path("subscribe/", subscribe_page, name="subscribe"),
    path("contact/", contact_page, name="contact"),

    # Legacy routes retained for backward compatibility
    path("News", news_page),
    path("Articles", article_page),
    path("Articles/<int:article_id>", article_detail_page),
    path("Interview", interview_page),
    path("Equipment", equipment_page),
    path("Events", events_page),
    path("Subscribe", subscribe_page),
    path("Contact", contact_page),
]