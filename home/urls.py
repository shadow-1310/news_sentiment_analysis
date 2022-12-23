from django.contrib import admin
from django.urls import path,include
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('make_article_db', views.make_article_db, name='make_article_db'),
    path('test', views.test, name='test'),
]