from email.policy import default
from enum import unique
from unittest.util import _MAX_LENGTH
from django.db import models
# from home.models import Genealogy

# Create your models here.

class UserInfo(models.Model):
    """
    用户：划分角色
    """
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=128)
    gender = models.CharField(max_length=1,default='0') #0男1女2保密
    nickname = models.CharField(max_length=32)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    addtime = models.DateTimeField(auto_now_add=True, verbose_name='加入时间')

    # 定义用户和角色的多对多关系
    roles = models.ManyToManyField("Role")

    # 定义用户的额外的权限
    permissions = models.ManyToManyField("Permission", blank=True)
    
    # 定义用户和族谱的多对多关系
    # genealogys =models.ManyToManyField("Genealogy")
    #删除标记:字符，0表示未删除，1表示删除
    is_del = models.CharField(max_length=1, default='0', verbose_name='删除标记')
    
    
    def __str__(self):
        return self.nickname

class AttachedUser(models.Model):
    #创建者
    create_by = models.ForeignKey(to=UserInfo, related_name='created_%(app_label)s_%(class)s_related', to_field='username', null=True, blank=True, on_delete=models.DO_NOTHING)

    #创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    #更新者
    update_by = models.ForeignKey(to=UserInfo, related_name='updated_%(app_label)s_%(class)s_related', to_field='username', null=True, blank=True, on_delete=models.DO_NOTHING)

    #更新时间
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        abstract = True


class Role(models.Model):
    """
    角色：绑定权限
    """
    title = models.CharField(max_length=32, unique=True)

    disc = models.CharField(max_length=50)
    # 定义角色和权限的多对多关系
    permissions = models.ManyToManyField("Permission")
    
    def __str__(self):
        return self.title

class Permission(models.Model):
    """
    权限
    """
    title = models.CharField(max_length=32, unique=True)
    url = models.CharField(max_length=1280, unique=True)
    menu = models.ForeignKey("Menu", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        # 显示带菜单前缀的权限
        return '{menu}---{permission}'.format(menu=self.menu, permission=self.title)

class Menu(AttachedUser):
    """
    菜单
    """
    title = models.CharField(max_length=32, unique=True)
    parent = models.ForeignKey("Menu", null=True, blank=True, on_delete=models.SET_NULL)    
    # 定义菜单间的自引用关系
    # 权限url 在 菜单下；菜单可以有父级菜单；还要支持用户创建菜单，因此需要定义parent字段（parent_id）
    # blank=True 意味着在后台管理中填写可以为空，根菜单没有父级菜单

    #排序
    order = models.IntegerField(null=True, blank=True, verbose_name='显示顺序')

    #类型 D目录菜单 M链接菜单 B按钮
    menu_type = models.CharField(max_length=1, null=True, blank=True, default='D', verbose_name='菜单类型')

    #打开方式 menuItem页签 menuBlank新窗口
    target = models.CharField(max_length=10, null=True, blank=True, default='menuItem', verbose_name='打开方式')

    #菜单显示隐藏
    visible = models.CharField(max_length=1, null=True, blank=True, default='1', verbose_name='是否隐藏')

    #图标
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name='打开方式')

    #描述
    disc = models.CharField(max_length=50)

    def __str__(self):
        # 显示层级菜单
        title_list = [self.title]
        p = self.parent
        while p:
            title_list.insert(0, p.title)
            p = p.parent
        return '-'.join(title_list)