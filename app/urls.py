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
# from app.settings import STATIC_ROOT

urlpatterns = [
    # re_path('media/(?P<path>.*)', serve, {'document_root': STATIC_ROOT}, name='media_url'),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('home', views.index, name='home'),
    path('index', views.index, name='index'),
    path('login1', views.login, name='login'),

    path('genealogy', views.genealogy, name='genealogy'),
    path('genealogy/del/<id>', views.genealogy_delete, name='delgene'),
    path('genealogy/apply', views.index, name='applygene'),
    path('genealogy/edit', views.genealogy_edit, name='editgene'),

    path('individual/<id>', views.individual, name='individual'),
    path('individual/add/<id>', views.individual_add, name='addindividual'),
    path('person/add/<id>', views.person_add, name='addperson'),
    path('person/delete/<gid>/<id>', views.person_delete, name='deleteperson'),

    path('keshihua', views.keshihua, name='keshihua'),
    path('DataToJson1/<id>', views.keshihua1, name='keshihua1'),

    path('file', views.index, name='file'),
    path('file/upload', views.file_upload, name='uploadfile'),
    path('file/uploader/<id>', views.file_uploader, name='fileuploader'),
    path('file/download', views.file_download, name='downloadfile'),
    path('file/downloader/<filename>', views.file_downloader, name='downloaderfile'),

    path('vis', views.index, name='vis'),
]
