
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='scrapper-home'),
    path('administrator', views.admin, name='scrapper-admin'),
    path('productlist', views.productlist, name='scrapper-productlist'),
    path('register', views.register, name='scrapper-register'),
    path('login', views.login, name='scrapper-login'),
    path('search', views.search, name='scrapper-search'),
]
