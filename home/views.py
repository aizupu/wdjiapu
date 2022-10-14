from django.shortcuts import render, redirect
from home.models import Genealogy, Docformat, Doctype
from home.models import Individual
from home.models import File
from home.models import Document
import time, datetime
import os


# Create your views here.

# ------------------------网站首页-----------------------
def index(request):
    return render(request, 'home/index.html')


def test(request):
    return render(request, 'home/test.html')


def about(request):
    return render(request, 'home/about.html')


def login(request):
    return render(request, 'home/login.html')


def logout(request):
    return render(request, 'home/index.html')


def register(request):
    return render(request, 'home/register.html')


# =========================与家谱相关的页面=========================
# 家谱首页
def genealogy(request):
    return render(request, 'genealogy/gene.html')


# 家谱详情
def genealogy_info(request, id):
    g = Genealogy.objects.get(id = id)
    return render(request, 'genealogy/gene_info.html',{'g':g})


# 我的家谱
def gene_list(request):
    g = Genealogy.objects.all().values()
    cnt = Genealogy.objects.all().count()
    for i in g:
        i['indi_sum'] = Individual.objects.filter(gene=i['title']).count()
        print(i['indi_sum'])
        i['file_sum'] = File.objects.filter(Genealogy=i['title']).count()
        i['doc_sum'] = Document.objects.filter(genealogy=i['title']).count()
    return render(request, 'genealogy/gene_list.html', {"genealogy": g, "count": cnt})
    return render(request, 'genealogy/gene_list.html')


# 创建家谱
def gene_add(request):
    return render(request, 'genealogy/gene_add.html')


def genealogy_add(request):
    genealogy_name = request.GET.get('gname')
    genealogy_sername = request.GET.get('sername')
    genealogy_location = request.GET.get('location')
    hall_name = request.GET.get('hall_title')
    county_title = request.GET.get('county_title')
    genealogy_item = Genealogy(title=genealogy_name, sername=genealogy_sername, hall_title=hall_name,
                               county_title=county_title, location=genealogy_location)
    genealogy_item.save()
    return redirect('/genealogy/list')


# 删除家谱：是一个请求，删除之后直接返回我的家谱页面
def gene_del(request, id):
    g = Genealogy.objects.get(id=id)
    g.delete()
    return redirect('/genealogy/list')


# 更新家谱：分为get和post，get定位到update的家谱编号；post之后直接返回我的家谱
def gene_upd(request):
    return render(request, 'genealogy/gene_upd.html')


# 查看详细的家谱：查看某个家谱的详细信息页面，
def gene_dtl(request, id):
    g = Genealogy.objects.get(id=id)
    print(g)
    p = Individual.objects.filter(gene=g.title)
    for i in p:
        print(i.ad_birth)
        print(datetime.datetime.strftime(i.ad_birth, '%Y-%m-%d %H:%M:%S'))
    print(p)
    d = Document.objects.filter(genealogy=g.title)
    f = File.objects.filter(Genealogy=g.title)
    return render(request, 'genealogy/gene_dtl.html', {"gid": id, "person": p, "document": d, "file": f})


# 生成某个家族的电子谱书
def gene_grt(request):
    return render(request, 'genealogy/gene_grt.html')


# =========================与人物相关的页面=========================
# 人物首页，列出某个家谱中的所有人物。
# 需要参数家谱ID，没有家谱ID，返回为空跳到家谱首页
def indi(request):
    return render(request, 'genealogy/indi.html')


# 添加人物
def indi_add(request, id):
    return render(request, 'genealogy/indi_add.html', {"gid": id})


def add_indi(request, id):
    surname = request.GET.get('gname')
    name = request.GET.get('name')
    zi = request.GET.get('zi')
    hao = request.GET.get('hao')
    gender = request.GET.get('gender')
    alive_flag = request.GET.get('alive_flag')
    line_name = request.GET.get('line_name')
    generetion = request.GET.get('generetion')
    rank = request.GET.get('rank')
    ad_birth = request.GET.get('ad_birth')
    ad_death = request.GET.get('ad_death')
    birth_place = request.GET.get('birth_place')
    death_place = request.GET.get('death_place')
    biography = request.GET.get('biography')
    epitaph = request.GET.get('epitaph')
    address = request.GET.get('address')
    genealogy = Genealogy.objects.get(id=id)
    individual_item = Individual(gene=genealogy, surname=surname, name=name, gender=gender, zi=zi, hao=hao, \
                                 line_name=line_name, generetion=generetion, rank=rank, is_alive=alive_flag,
                                 ad_birth=ad_birth, ad_death=ad_death, birth_place=birth_place, \
                                 death_place=death_place, biography=biography, epitaph=epitaph, address=address)
    individual_item.save()

    return redirect('/genealogy/dtl/' + id)


# 删除人物：是一个请求，删除之后直接返回人物首页页面
def indi_del(request,gid,id):
    p = Individual.objects.get(id = id)
    p.delete()
    return redirect('/genealogy/dtl/' + gid)

# 添加人物关系
def indi_rel(request):
    return render(request, 'genealogy/indi_rel.html')


# 查看详细的人物：查看某个人物的详细信息页面，
def indi_dtl(request,id):
    p = Individual.objects.get(id = id)
    return render(request, 'genealogy/indi_dtl.html',{'p':p})


# 查看人物树
def indi_tree(request):
    return render(request, 'genealogy/indi_tree.html')


# =========================与文档相关的页面=========================
# 文档首页
def doc(request):
    return render(request, 'genealogy/doc.html')


# 添加文档
def doc_add(request, id):
    return render(request, 'genealogy/doc_add.html', {"gid": id})


def doc_submit(request, id):
    genealogy = Genealogy.objects.get(id=id)
    title = request.GET.get('gname')
    author = request.GET.get('hall_title')
    format_str = request.GET.get('dformat')
    doc_format = Docformat.objects.filter(title=format_str)
    if len(doc_format) == 0:
        doc_fitem = Docformat(title=format_str)
        doc_fitem.save()
    else:
        doc_fitem = doc_format[0]
    type_str = request.GET.get('dtype')
    doc_type = Doctype.objects.filter(title=type_str)
    if len(doc_type) == 0:
        doc_titem = Doctype(title=type_str)
        doc_titem.save()
    else:
        doc_titem = doc_type[0]
    doc_rank = request.GET.get('drank')
    doc_content = request.GET.get('content')
    doc_item = Document(title=title, author=author, docformat=doc_fitem, doctype=doc_titem, content=doc_content,
                        rank=doc_rank, genealogy=genealogy)
    doc_item.save()
    return redirect('/genealogy/dtl/' + id)


# 删除文档：是一个请求，删除之后直接返回当前族谱的文档首页
def doc_del(request,gid,id):
    d = Document.objects.get(id = id)
    d.delete()
    return redirect('/genealogy/dtl/' + gid)

# 更新文档：分为get和post，get定位到update的文档编号；post之后直接返回家谱文档首页
def doc_upd(request):
    return render(request, 'genealogy/doc_upd.html')

# 查看详细的文档：查看某个文档的详细信息页面，
def doc_dtl(request,id):
    d = Document.objects.get(id=id)
    return render(request, 'genealogy/doc_dtl.html',{'d':d})


# =========================与PDF文件相关的页面=========================
# 文件首页
def file(request):
    return render(request, 'genealogy/file.html')


# 添加文件
def file_add(request, id):
    title = request.GET.get('name')
    file = request.FILES.get('inputfile')
    if file:
        basedir = os.path.abspath(os.path.join(os.path.dirname("__file__")))
        file_path = os.path.join(basedir, 'static','files', file.name)
        f=open(file_path,'wb+')
        for chunk in file.chunks():
            f.write(chunk)
        f.close()
        genealogy = Genealogy.objects.get(id = id)
        file_item = File(filename=file.name, path=file_path, Genealogy=genealogy)
        file_item.save()

    return redirect('/genealogy/dtl/'+id)


# 删除文件：是一个请求，删除之后直接返回当前家谱的文件首页页面
def file_del(request,gid,id):
    File.objects.filter(id=id).update(is_del='1')
    return redirect('/genealogy/dtl/' + gid)


# 更新文件：分为get和post，get定位到update的文件编号；post之后直接返回当前家谱的文件首页页面
def file_upd(request):
    return render(request, 'genealogy/file_upd.html')


# 查看详细的文件：查看某个文件的详细信息页面，
def file_dtl(request):
    return render(request, 'genealogy/file_dtl.html')


# 文件下载，需要检查权限
def file_dwn(request,id):
    f = File.objects.get(id = id)
    basedir = os.path.abspath(os.path.join(os.path.dirname("__file__")))
    file_path = os.path.join(basedir, 'static','files', f.filename)
    response = FileResponse(open(file_path, "rb"))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename='+f.filename
    return response


# =========================与可视化相关的页面=========================
# 可视化首页
def vis(request):
    return render(request, 'vis/vis.html')
