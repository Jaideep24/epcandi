from django.urls import path
from .views import *
urlpatterns=[
    path("", home_page, name="home"),
    path("news/", news_page, name="news"),
    path("news/<int:news_id>/", news_detail_page, name="news-detail"),
    path("focus/<int:focus_id>/", focus_detail_page, name="focus-detail"),
    path("articles/<int:article_id>/", article_detail_page, name="article-detail"),
    path("guest-articles/<int:guest_article_id>/", guest_article_detail_page, name="guest-article-detail"),
    path("interview/<int:interview_id>/", interview_detail_page, name="interview-detail"),
    path("equipment/", equipment_page, name="equipment"),
    path("equipment/<int:equipment_id>/", equipment_detail_page, name="equipment-detail"),
    path("events/", events_page, name="events"),
    path("events/<int:event_id>/", event_detail_page, name="event-detail"),
    path("subscribe/", subscribe_page, name="subscribe"),
    path("contact/", contact_page, name="contact"),
    path("focus/", focus_page, name="focus"),
    path("shopping-cart/", shopping_cart_page, name="shopping_cart"),
    path("guest-article/", guest_article_page, name="guest_article"),
    path("square-foot/", square_foot_page, name="square_foot"),
    path("about/", about_page, name="about"),
    path("disclaimer/", disclaimer_page, name="disclaimer"),
    path("privacy/", privacy_page, name="privacy"),

]