from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('user', views.login, name='user'),
    path('logout', views.login, name='logout'),
    path('main', views.main, name='main'),
    path('', views.login, name='login'),
    path('', views.login, name='login'),
    path('', views.login, name='login'),
]