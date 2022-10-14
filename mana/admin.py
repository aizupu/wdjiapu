from django.contrib import admin

from .models import UserInfo, Role, Permission, Menu
# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(Menu)