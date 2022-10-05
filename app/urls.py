"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from home import views

from django.views.static import serve
from app.settings import STATIC_ROOT

urlpatterns = [
    re_path('media/(?P<path>.*)', serve, {'document_root': STATIC_ROOT}, name='media_url'),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('home', views.index, name='home'),
    path('index', views.index, name='index'),

    path('genealgoy', views.index, name='genealgoy'),
    path('genealgoy/del', views.index, name='delgene'),
    path('genealgoy/apply', views.index, name='applygene'),
    path('genealgoy/edit', views.index, name='editgene'),

    path('individual', views.index, name='individual'),

    path('file', views.index, name='file'),
    path('file/upload', views.index, name='uploadfile'),
    path('file/down', views.index, name='downfile'),

    path('vis', views.index, name='vis'),
]
