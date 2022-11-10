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
from mana import views as mana_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('home', views.index, name='home'),
    path('index', views.index, name='index'),
    path('test', views.test, name='test'),
    path('about', views.about, name='about'),
    path('achievement', views.achievement, name='achievement'),
    path('login', mana_views.login, name='login'),
    path('login_submit',mana_views.login_submit, name='login_submit'),
    path('logout', mana_views.logout, name='logout'),
    path('register', mana_views.register, name='register'),
    path('register_submit', mana_views.register_submit,name='register_submit'),
    path('upadte_passwd', mana_views.upd_passwd, name='upadte_passwd'),
    path('upd_passwd_submit', mana_views.upd_passwd_submit, name='upd_passwd_submit'),
    path('upadte_userinfo', mana_views.upd_userinfo, name='upadte_userinfo'),
    path('upd_userinfo_submit', mana_views.upd_userinfo_submit, name='upadte_userinfo_submit'),
    path('user/list', mana_views.user_list,name='user_list'),
    path('user/add',mana_views.u_add,name='u_add'),
    path('user/add_user',mana_views.user_add,name='user_add'),
    path('user/del/<id>',mana_views.user_del,name='user_del'),

    #=========================与家谱相关的页面=========================
    path('genealogy', views.genealogy, name='genealogy'),
    path('genealogy/info/<id>', views.genealogy_info, name='genealogy_info'),
    path('genealogy/list', views.gene_list, name='gene_list'),
    path('genealogy/add', views.gene_add, name='gene_add'),
    path('genealogy/add_genealogy', views.genealogy_add, name='genealogy_add'),
    path('genealogy/del/<id>', views.gene_del, name='gene_del'),
    path('genealogy/upd/<id>', views.gene_upd, name='gene_upd'),
    path('genealogy/dtl/<id>', views.gene_dtl, name='gene_dtl'),
    path('genealogy/dtl_doc/<id>', views.gene_doc, name='gene_doc'),
    path('genealogy/dtl_pdf/<id>', views.gene_pdf, name='gene_pdf'),
    path('genealogy/grt/<id>', views.gene_grt, name='gene_grt'),
    path('genealogy/search', views.gene_search, name='gene_search'),

    #=========================与人物相关的页面=========================
    path('genealogy/indi', views.indi, name='indi'),
    path('genealogy/indi/add/<id>', views.indi_add, name='indi_add'),
    path('genealogy/indi/add_indi/<id>', views.add_indi, name='add_indi'),
    path('genealogy/indi/add_parent/<id>', views.add_parent, name='add_parent'),
    path('genealogy/indi/add_spouse/<id>', views.add_spouse, name='add_spouse'),
    path('genealogy/indi/add_child/<id>', views.add_child, name='add_child'),
    path('genealogy/indi/submit_parent/<id>', views.submit_parent, name='submit_parent'),
    path('genealogy/indi/submit_spouse/<id>', views.submit_spouse, name='submit_spouse'),
    path('genealogy/indi/submit_child/<id>', views.submit_child, name='submit_child'),
    path('genealogy/indi/del/<gid>/<id>', views.indi_del, name='indi_del'),
    path('genealogy/indi/upd/<id>', views.indi_upd, name='indi_upd'),
    path('genealogy/indi/dtl/<id>', views.indi_dtl, name='indi_dtl'),
    path('genealogy/indi/search/<id>', views.indi_search, name='indi_search'),
    path('genealogy/indi/tree', views.indi_tree, name='indi_tree'),

    # =========================与文档相关的页面=========================
    path('genealogy/doc', views.doc, name='doc'),
    path('genealogy/doc/add/<id>', views.doc_add, name='doc_add'),
    path('genealogy/doc/add/submit/<id>', views.doc_submit, name='doc_submit'),
    path('genealogy/doc/del/<gid>/<id>', views.doc_del, name='doc_del'),
    path('genealogy/doc/upd', views.doc_upd, name='doc_upd'),
    path('genealogy/doc/dtl/<id>', views.doc_dtl, name='doc_dtl'),
    path('genealogy/doc/search', views.search_doc, name='search_doc'),
    path('genealogy/doc/search/<id>', views.doc_search, name='doc_search'),
    
    #=========================与PDF文件相关的页面=========================
    path('genealogy/file', views.file, name='file'),
    path('genealogy/file/add/<id>', views.file_add, name='file_add'),
    path('genealogy/file/del/<gid>/<id>', views.file_del, name='file_del'),
    path('genealogy/file/upd', views.file_upd, name='file_upd'),
    path('genealogy/file/dtl', views.file_dtl, name='file_dtl'),
    path('genealogy/file/download/<id>', views.file_dwn, name='file_dwn'),
    path('genealogy/file/view/<id>', views.file_view, name='file_view'),
    path('genealogy/file/search', views.search_file, name='search_file'),
    path('genealogy/file/search/<id>', views.file_search, name='file_search'),

    #=========================与指导说明相关的页面=========================
    path('guide/gene', views.guide_gene, name='guide_gene'),
    path('guide/indi', views.guide_indi, name='guide_indi'),
    path('guide/doc', views.guide_doc, name='guide_doc'),
    path('guide/permission', views.guide_permission, name='guide_permission'),
    
    #=========================与可视化相关的页面=========================
    path('vis', views.vis, name='vis'),
    
    #=========================管理后台=========================
    re_path(r'^mana/', include('mana.urls'))
]
