from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path("",homepage),
    path("News",Newspage),
    path("Articles",Articlepage),
    path("Interview",Interviewpage),
    path("Equipment",Equipmentpage)
]