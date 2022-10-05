from django.db import models

from mana.models import AttachedUser

# Create your models here.

class Genealogy(AttachedUser):
    '''
    家谱：

    '''
    #标题
    title = models.CharField(max_length=50, unique=True, verbose_name='标题')

    #姓氏
    sername = models.CharField(max_length=10, verbose_name='姓氏')

    #堂号
    hall_title = models.CharField(max_length=10, blank=True, verbose_name='堂号')

    #郡望
    county_title = models.CharField(max_length=10, blank=True, verbose_name='郡望号')

    #位置
    location = models.CharField(max_length=50, blank=True, verbose_name='位置')

    #联系人
    contact = models.CharField(max_length=10, blank=True, verbose_name='联系人')

    #联系电话
    contact_phone = models.CharField(max_length=13, blank=True, verbose_name='联系电话')

    #备注
    note = models.CharField(max_length=500, blank=True, verbose_name='备注')

    #是否公开：字符，0公开，1私有
    is_public = models.CharField(max_length=32, default='0', verbose_name='是否公开')

    #访问密码
    access_pwd = models.CharField(max_length=8, blank=True, verbose_name='访问密码')
    
    #删除标记:字符，0表示未删除，1表示删除
    is_del = models.CharField(max_length=1, default='0', verbose_name='删除标记')


    def __str__(self):
        return self.title

class Individual(AttachedUser):
    '''
    人物：
    '''
    #所属族谱
    gene = models.ForeignKey("Genealogy", related_name='indi_genealogy',  to_field='title',  null=True, blank=True, on_delete=models.SET_NULL)

    #姓
    surname = models.CharField(max_length=10, unique=False, verbose_name='姓')

    #名
    name = models.CharField(max_length=10, unique=False, verbose_name='名')

    #字
    zi = models.CharField(max_length=10, unique=False, verbose_name='字')

    #号
    hao = models.CharField(max_length=10, unique=False, verbose_name='号')

    #常用名
    common_name = models.CharField(max_length=10, unique=False, verbose_name='常用名')

    #性别  0男 1女 2保密
    gender = models.CharField(max_length=1, unique=False, default='0', verbose_name='性别')

    #父亲
    farther = models.ForeignKey("Individual", related_name='indi_farther', null=True, blank=True, on_delete=models.SET_NULL)

    #母亲
    mother = models.ForeignKey("Individual", related_name='indi_mother', null=True, blank=True, on_delete=models.SET_NULL)

    #配偶
    spouse = models.ForeignKey("Individual", related_name='indi_spouse', null=True, blank=True, on_delete=models.SET_NULL)

    #公元纪年出生日期
    ad_birth = models.DateTimeField(null=True, blank=True, verbose_name='公元出生日期')

    #年号纪年出生日期
    ce_birth = models.CharField(max_length=32, unique=False, verbose_name='年号出生日期')

    #出生地
    birth_place = models.CharField(max_length=50, unique=False, verbose_name='出生地')

    #公元纪年逝世日期
    ad_death = models.DateTimeField(null=True, blank=True, verbose_name='公元逝世日期')

    #年号纪年逝世日期
    ce_death = models.CharField(max_length=32, unique=False, verbose_name='年号逝世日期')

    #逝世地
    death_place = models.CharField(max_length=50, unique=False, verbose_name='逝世地')

    #家族排行
    line_name = models.CharField(max_length=2, unique=False, verbose_name='家族排行')

    #世代数
    generetion = models.CharField(max_length=2, unique=False, verbose_name='世代数')

    #出生排行
    rank = models.CharField(max_length=32, unique=False, verbose_name='出生排行')

    #是否健在  0去世  1健在  2未知
    is_alive = models.CharField(max_length=1, unique=False, verbose_name='是否健在')

    #生平简介
    biography = models.CharField(max_length=1000, unique=False, verbose_name='生平简介')

    #墓志铭
    epitaph = models.CharField(max_length=1000, unique=False, verbose_name='墓志铭')

    #身份证号
    idcard_no = models.CharField(max_length=18, unique=True, verbose_name='身份编号')

    #地址
    address = models.CharField(max_length=50, unique=False, verbose_name='住址')

    #电话号码
    phone = models.CharField(max_length=11, unique=False, verbose_name='电话号码')

    #身份类型
    idcard_type = models.CharField(max_length=32, default='居民身份证', verbose_name='身份证')

    #是否删除
    is_del = models.CharField(max_length=1, default='0', verbose_name='删除标记')

    #备注
    note = models.CharField(max_length=500, unique=False, verbose_name='')

    def __str__(self):
        return self.surname + self.name

#上传的文件
class File(models.Model):
    '''
    上传的pdf文件
    '''
    filename = models.CharField(max_length=50, unique=False, verbose_name='')

    path = models.CharField(max_length=50, unique=False, verbose_name='')

    Genealogy = models.ForeignKey('Genealogy', to_field='title',  null=True, blank=True, on_delete=models.DO_NOTHING)

    #是否删除
    is_del = models.CharField(max_length=1, default='0', verbose_name='删除标记')

    def __str__(self):
        return self.filename

class Docformat(models.Model):
    '''
    文档格式：文本、图片、视频、音频等
    '''
    #标题
    title = models.CharField(max_length=10, unique=True, verbose_name='')

    #描述
    disc = models.CharField(max_length=50, unique=False, verbose_name='')

    #排序，不同格式之间的排序
    order = models.CharField(max_length=2, unique=False, verbose_name='')

    def __str__(self):
        return self.filename

class Doctype(models.Model):
    '''
    文档类型：源流、艺文、传记、田产地契等
    '''
    #标题
    title = models.CharField(max_length=10, unique=True, verbose_name='')

    #描述
    disc = models.CharField(max_length=50, unique=False, verbose_name='')

    #排序，不同文档类型的排序
    order = models.CharField(max_length=2, unique=False, verbose_name='')

    def __str__(self):
        return self.filename

class Document(models.Model):
    '''
    可编辑文档
    '''
    #标题
    title = models.CharField(max_length=50, unique=False, verbose_name='')

    #作者
    author = models.CharField(max_length=10, unique=False, verbose_name='')

    #格式
    docformat = models.ForeignKey('Docformat', to_field='title', null=True, blank=True, on_delete=models.DO_NOTHING)

    #类型
    doctype = models.ForeignKey('Doctype', to_field='title', null=True, blank=True, on_delete=models.DO_NOTHING)

    #内容
    content = models.CharField(max_length=5000, unique=False, verbose_name='')

    #排序
    rank = models.CharField(max_length=500, unique=False, verbose_name='')

    #所属族谱
    genealogy = models.ForeignKey('Genealogy', to_field='title', null=True, blank=True, verbose_name='', on_delete=models.DO_NOTHING)

    #是否删除
    is_del = models.CharField(max_length=1, default='0', verbose_name='删除标记')

    #是否可见
    visible = models.CharField(max_length=1, default='1', verbose_name='是否可见')

    def __str__(self):
        return ''