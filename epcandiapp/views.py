from django.shortcuts import render
from .models import *
# Create your views here.

def homepage(request):
    return(render(request,"epcandiapp/Inder.html",{"News":News.objects.all().values(),"Articles":Articles.objects.all().values(),"Interviews":Interview.objects.all().values(),"Equipment_News":Equipment_News.objects.all().values}))
def Newspage(request):
    return(render(request,"epcandiapp/News.html",{"News":News.objects.all().values()}))
def Articlepage(request):
    return(render(request,"epcandiapp/Articles.html",{"Articles":Articles.objects.all().values()}))
def Interviewpage(request):
    return(render(request,"epcandiapp/Interview.html",{"Interviews":Interview.objects.all().values()}))
def Equipmentpage(request):
    return(render(request,"epcandiapp/Equipment News.html",{"Equipment_News":Equipment_News.objects.all().values()}))