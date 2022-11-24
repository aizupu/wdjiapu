from django.contrib import admin
from .models import Genealogy, Individual, File, Docformat, Doctype, Document
# Register your models here.
# admin.site.register(Genealogy)
admin.site.register(Individual)
admin.site.register(File)
admin.site.register(Docformat)
admin.site.register(Doctype)
admin.site.register(Document)

# 家谱内容
@admin.register(Genealogy)
class GenealogyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'sername', 'hall_title', 'county_title', 'location', 'create_time')
    # 文章列表里显示想要显示的字段
    list_per_page = 30
    # 满50条数据就自动分页
    ordering = ('-create_time',)
    # 后台数据列表排序方式
    list_display_links = ('id', 'title')
    # 设置哪些字段可以点击进入编辑界面