from django.shortcuts import render, redirect
from django.utils.encoding import escape_uri_path
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from home.util import split_page,change_info
from home.models import Genealogy, Docformat, Doctype
from home.models import UserIP, VisitNumber, DayNumber
from home.models import Individual
from home.models import File
from home.models import Document
from generate.family_tree import FamilyTree
from generate.line_biography import LineBiography
from generate.util import mergeHzAndDxt
from generate.web2local import web2local
from app.settings import PDF_OUTPUT_PATH
from django.http import FileResponse
import time, datetime
import os
# Create your views here.

# ------------------------网站首页-----------------------
def index(request):
    change_info(request,'/')
    gcnt = Genealogy.objects.filter(is_del='0').count()
    scnt = Genealogy.objects.filter(is_del='0').values('sername').distinct().count()
    pcnt =  Individual.objects.filter(is_del='0').count()
    total_visit = VisitNumber.objects.get(id=1)
    today_visit = DayNumber.objects.get(day=datetime.date.today())
    return render(request, 'home/index.html',{"gcnt":gcnt,"scnt":scnt,"pcnt":pcnt,"total_visit":total_visit,"today_visit":today_visit})


def test(request):
    
    return render(request, 'home/test.html')


def about(request):
    return render(request, 'home/about.html')


def achievement(request):
    return render(request, 'home/achievement.html')


# =========================与家谱相关的页面=========================
# 家谱首页
def genealogy(request):
    # if 'logged_in' in request.session and request.session['logged_in']:
    #     return render(request, 'genealogy/gene.html')
    # else:
    #     return render(request, 'home/login.html')
    return render(request, 'genealogy/gene.html')


# 家谱详情
def genealogy_info(request, id):
    g = Genealogy.objects.get(id=id)
    return render(request, 'genealogy/gene_info.html', {'g': g})


# 我的家谱
def gene_list(request):
    g = Genealogy.objects.all().values()
    cnt = Genealogy.objects.filter(is_del='0').count()
    for i in g:
        i['indi_sum'] = Individual.objects.filter(gene=i['title'],is_del='0').count()
        i['file_sum'] = File.objects.filter(Genealogy=i['title'],is_del='0').count()
        i['doc_sum'] = Document.objects.filter(genealogy=i['title'],is_del='0').count()
    page,paginator,dis_range = split_page(request,g)
    return render(request, 'genealogy/gene_list.html', {"genealogy":page, "count": cnt,"g_cnt":cnt, 'page': page, 'paginator': paginator, 'dis_range': dis_range})


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
    Genealogy.objects.filter(id=id).update(is_del = '1')
    return redirect('/genealogy/list')


# 更新家谱：分为get和post，get定位到update的家谱编号；post之后直接返回我的家谱
def gene_upd(request,id):
    g = Genealogy.objects.get(id=id)
    g.sername = request.GET.get('sername')
    g.hall_title = request.GET.get('hall_title')
    g.county_title = request.GET.get('county_title')
    g.location = request.GET.get('location')
    g.save()
    return redirect('/genealogy/list')


# 查看详细的家谱：查看某个家谱的详细信息页面，
def gene_dtl(request, id):
    g = Genealogy.objects.get(id=id)
    p = Individual.objects.filter(gene=g.title,is_del='0')
    p_cnt = p.count()
    page,paginator,dis_range = split_page(request,p)
    return render(request, 'genealogy/gene_dtl.html', {"g":g, "gid": id, "person": page, "cnt":p_cnt, "p_cnt":p_cnt, 'page': page, 'paginator': paginator, 'dis_range': dis_range})

def gene_doc(request, id):
    g = Genealogy.objects.get(id=id)
    d = Document.objects.filter(genealogy=g.title,is_del='0').order_by("rank")
    d_cnt = d.count()
    page,paginator,dis_range = split_page(request,d)
    return render(request, 'genealogy/gene_dtl_doc.html', {"g":g, "gid": id, "document": page, "d_cnt":d_cnt, "cnt":d_cnt, 'page': page, 'paginator': paginator, 'dis_range': dis_range})

def gene_pdf(request,id):
    g = Genealogy.objects.get(id=id)
    f = File.objects.filter(Genealogy=g.title,is_del='0')
    f_cnt = f.count()
    page,paginator,dis_range = split_page(request,f)
    return render(request, 'genealogy/gene_dtl_pdf.html', {"g":g, "gid": id, "file": page, "f_cnt":f_cnt, "cnt":f_cnt, 'page': page, 'paginator': paginator, 'dis_range': dis_range})

# 生成某个家族的电子谱书
def gene_grt(request, id):
    zp_id, zp_name = web2local(id)
    print("---数据库转换结束---")
    # 生成
    LineBiography(zp_id)
    print("---行传生成完成---")
    FamilyTree(zp_id)
    print("---吊线图生成完成---")
    pdf_path = mergeHzAndDxt(zp_name)
    print("---合并完成---")
    file_path = os.path.join(PDF_OUTPUT_PATH, zp_name, pdf_path)
    response = FileResponse(open(file_path, "rb"))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(pdf_path))
    return response

def gene_search(request):
    # if 'logged_in' not in request.session or request.session['logged_in']!=True:
    #     return render(request, 'home/login.html') 
    name = request.GET.get('name')
    g = Genealogy.objects.filter(is_del='0',title__contains=name).values()
    cnt = Genealogy.objects.filter(is_del='0').count()
    g_cnt = g.count()
    for i in g:
        i['indi_sum'] = Individual.objects.filter(gene=i['title']).count()
        i['file_sum'] = File.objects.filter(Genealogy=i['title']).count()
        i['doc_sum'] = Document.objects.filter(genealogy=i['title']).count()
    page,paginator,dis_range = split_page(request,g)
    return render(request, 'genealogy/gene_list.html', {"genealogy":page, "name":name, "count": cnt, "g_cnt":g_cnt, 'page': page, 'paginator': paginator, 'dis_range': dis_range})



# =========================与人物相关的页面=========================
# 人物首页，列出某个家谱中的所有人物。
# 需要参数家谱ID，没有家谱ID，返回为空跳到家谱首页
def indi(request):
    return render(request, 'genealogy/indi.html')


# 添加人物
def indi_add(request, id):
    return render(request, 'genealogy/indi_add.html', {"gid": id})

def add_parent(request,id):
    p = Individual.objects.get(id = id)
    return render(request, 'genealogy/add_parent.html', {"p":p})

def add_spouse(request,id):
    p = Individual.objects.get(id = id)
    return render(request, 'genealogy/add_spouse.html', {"p":p})

def add_child(request,id):
    p = Individual.objects.get(id = id)
    return render(request, 'genealogy/add_child.html', {"p":p})

def submit_parent(request,id):
    p =  Individual.objects.get(id = id)
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
    ce_birth = request.GET.get('ce_birth')
    ad_death = request.GET.get('ad_death')
    ce_death = request.GET.get('ce_birth')
    birth_place = request.GET.get('birth_place')
    death_place = request.GET.get('death_place')
    biography = request.GET.get('biography')
    epitaph = request.GET.get('epitaph')
    address = request.GET.get('address')
    individual_item = Individual(gene=p.gene, surname=surname, name=name, gender=gender, zi=zi, hao=hao, \
                                 line_name=line_name, generetion=generetion, rank=rank, is_alive=alive_flag,
                                 ce_birth=ce_birth, ce_death=ce_death, birth_place=birth_place, \
                                 death_place=death_place, biography=biography, epitaph=epitaph, address=address)
    individual_item.save()
    if(ad_birth):
        individual_item.ad_birth=ad_birth
        individual_item.save()
    if(ad_death):
        individual_item.ad_death=ad_death
        individual_item.save()
    if gender == '0':
        p.farther = individual_item
    else:
        p.mother = individual_item
    p.save()
    return redirect('/genealogy/dtl/' + str(p.gene.id))

def submit_spouse(request,id):
    p =  Individual.objects.get(id = id)
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
    ce_birth = request.GET.get('ce_birth')
    ad_death = request.GET.get('ad_death')
    ce_death = request.GET.get('ce_birth')
    birth_place = request.GET.get('birth_place')
    death_place = request.GET.get('death_place')
    biography = request.GET.get('biography')
    epitaph = request.GET.get('epitaph')
    address = request.GET.get('address')
    individual_item = Individual(gene=p.gene, surname=surname, name=name, gender=gender, zi=zi, hao=hao, \
                                 line_name=line_name, generetion=generetion, rank=rank, is_alive=alive_flag,
                                 ce_birth=ce_birth, ce_death=ce_death, birth_place=birth_place, spouse = p,\
                                 death_place=death_place, biography=biography, epitaph=epitaph, address=address)
    individual_item.save()
    if(ad_birth):
        individual_item.ad_birth=ad_birth
        individual_item.save()
    if(ad_death):
        individual_item.ad_death=ad_death
        individual_item.save()
    p.spouse = individual_item
    p.save()
    return redirect('/genealogy/dtl/' + str(p.gene.id))

def submit_child(request,id):
    p =  Individual.objects.get(id = id)
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
    ce_birth = request.GET.get('ce_birth')
    ad_death = request.GET.get('ad_death')
    ce_death = request.GET.get('ce_birth')
    birth_place = request.GET.get('birth_place')
    death_place = request.GET.get('death_place')
    biography = request.GET.get('biography')
    epitaph = request.GET.get('epitaph')
    address = request.GET.get('address')
    if p.gender == '0':
        individual_item = Individual(gene=p.gene, surname=surname, name=name, gender=gender, zi=zi, hao=hao, \
                                 line_name=line_name, generetion=generetion, rank=rank, is_alive=alive_flag,
                                 ce_birth=ce_birth, ce_death=ce_death, birth_place=birth_place, farther = p,\
                                 death_place=death_place, biography=biography, epitaph=epitaph, address=address)
    else:
        individual_item = Individual(gene=p.gene, surname=surname, name=name, gender=gender, zi=zi, hao=hao, \
                                 line_name=line_name, generetion=generetion, rank=rank, is_alive=alive_flag,
                                 ce_birth=ce_birth, ce_death=ce_death, birth_place=birth_place, mother = p,\
                                 death_place=death_place, biography=biography, epitaph=epitaph, address=address)

    individual_item.save()
    if(ad_birth):
        individual_item.ad_birth=ad_birth
        individual_item.save()
    if(ad_death):
        individual_item.ad_death=ad_death
        individual_item.save()
    return redirect('/genealogy/dtl/' + str(p.gene.id))

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
    ce_birth = request.GET.get('ce_birth')
    ad_death = request.GET.get('ad_death')
    ce_death = request.GET.get('ce_birth')
    birth_place = request.GET.get('birth_place')
    death_place = request.GET.get('death_place')
    cemetery =  request.GET.get('cemetery')
    biography = request.GET.get('biography')
    epitaph = request.GET.get('epitaph')
    address = request.GET.get('address')
    genealogy = Genealogy.objects.get(id=id)
    individual_item = Individual(gene=genealogy, surname=surname, name=name, gender=gender, zi=zi, hao=hao, \
                                 line_name=line_name, generetion=generetion, rank=rank, is_alive=alive_flag,
                                 ce_birth=ce_birth, ce_death=ce_death, birth_place=birth_place, cemetery=cemetery,\
                                 death_place=death_place, biography=biography, epitaph=epitaph, address=address)
    individual_item.save()
    if(ad_birth):
        individual_item.ad_birth=ad_birth
        individual_item.save()
    if(ad_death):
        individual_item.ad_death=ad_death
        individual_item.save()
    return redirect('/genealogy/dtl/' + id)

# 删除人物：是一个请求，删除之后直接返回人物首页页面
def indi_del(request, gid, id):
    Individual.objects.filter(id=id).update(is_del='1')
    return redirect('/genealogy/dtl/' + gid)


# 更新人物信息
def indi_upd(request,id):
    individual_item = Individual.objects.get(id = id)
    individual_item.surname = request.GET.get('gname')
    individual_item.name = request.GET.get('name')
    individual_item.zi = request.GET.get('zi')
    individual_item.hao = request.GET.get('hao')
    individual_item.gender = request.GET.get('gender')
    individual_item.is_alive = request.GET.get('alive_flag')
    individual_item.line_name = request.GET.get('line_name')
    individual_item.generetion = request.GET.get('generetion')
    individual_item.rank = request.GET.get('rank')
    ad_birth = request.GET.get('ad_birth')
    individual_item.ce_birth = request.GET.get('ce_birth')
    ad_death = request.GET.get('ad_death')
    individual_item.ce_death = request.GET.get('ce_birth')
    individual_item.birth_place = request.GET.get('birth_place')
    individual_item.death_place = request.GET.get('death_place')
    individual_item.cemetery =  request.GET.get('cemetery')
    individual_item.biography = request.GET.get('biography')
    individual_item.epitaph = request.GET.get('epitaph')
    individual_item.address = request.GET.get('address')
    if(ad_birth):
        individual_item.ad_birth=ad_birth
    if(ad_death):
        individual_item.ad_death=ad_death
    individual_item.save()
    return redirect('/genealogy/dtl/' + str(individual_item.gene.id))

# 查看详细的人物：查看某个人物的详细信息页面，
def indi_dtl(request, id):
    p = Individual.objects.get(id=id)
    return render(request, 'genealogy/indi_dtl.html', {'p': p})

def indi_search(request, id):
    g = Genealogy.objects.get(id=id)
    name = request.GET.get('name')
    p = Individual.objects.filter(gene = g.title, name__contains=name, is_del='0')
    p_cnt = p.count()
    cnt = Individual.objects.filter(gene=g.title,is_del='0').count()
    page,paginator,dis_range = split_page(request,p)
    return render(request, 'genealogy/gene_dtl.html', {"g":g, "gid": id, "person": page, "name":name, "cnt":cnt, "p_cnt":p_cnt, 'page': page, 'paginator': paginator, 'dis_range': dis_range})

# 查看人物树
def indi_tree(request):
    return render(request, 'genealogy/indi_tree.html')


# =========================与文档相关的页面=========================
# 文档首页
def doc(request):
    d = Document.objects.filter(is_del='0')
    d_cnt = d.count()
    page,paginator,dis_range = split_page(request,d)
    return render(request, 'genealogy/doc.html', {"document": page, "d_cnt":d_cnt, "cnt":d_cnt, 'page': page, 'paginator': paginator, 'dis_range': dis_range})


# 添加文档
def doc_add(request, id):
    return render(request, 'genealogy/doc_add.html', {"gid": id})


def doc_submit(request, id):
    genealogy = Genealogy.objects.get(id=id)
    title = request.GET.get('gname')
    author = request.GET.get('hall_title')
    format_str = request.GET.get('dformat')
    dtime = request.GET.get('dtime')
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
                        time=dtime, rank=doc_rank, genealogy=genealogy)
    doc_item.save()
    return redirect('/genealogy/dtl/' + id)


# 删除文档：是一个请求，删除之后直接返回当前族谱的文档首页
def doc_del(request, gid, id):
    Document.objects.filter(id=id).update(is_del='1')
    return redirect('/genealogy/dtl/' + gid)


# 更新文档：分为get和post，get定位到update的文档编号；post之后直接返回家谱文档首页
def doc_upd(request):
    return render(request, 'genealogy/doc_upd.html')


# 查看详细的文档：查看某个文档的详细信息页面，
def doc_dtl(request, id):
    d = Document.objects.get(id=id)
    return render(request, 'genealogy/doc_view.html', {"d": d})

#在给定族谱中查找文档
def doc_search(request,id):
    g = Genealogy.objects.get(id=id)
    name = request.GET.get('name')
    cnt = Document.objects.filter(genealogy=g.title,is_del='0').count()
    d = Document.objects.filter(genealogy=g.title,title__contains=name,is_del='0')
    d_cnt = d.count()
    page,paginator,dis_range = split_page(request,d)
    return render(request, 'genealogy/gene_dtl_doc.html', {"g":g, "gid": id, "document": page, "name":name, "d_cnt":d_cnt, "cnt":cnt, 'page': page, 'paginator': paginator, 'dis_range': dis_range})

#在所有文档中查找文档
def search_doc(request):
    name = request.GET.get('name')
    cnt = Document.objects.all().count()
    d = Document.objects.filter(title__contains=name,is_del='0')
    d_cnt = d.count()
    page,paginator,dis_range = split_page(request,d)
    return render(request, 'genealogy/doc.html', {"document": page, "d_cnt":d_cnt, "cnt":cnt, 'page': page, "name":name, 'paginator': paginator, 'dis_range': dis_range})

# =========================与PDF文件相关的页面=========================
# 文件首页
def file(request):
    f = File.objects.filter(is_del='0')
    f_cnt = f.count()
    page,paginator,dis_range = split_page(request,f)
    return render(request, 'genealogy/file.html', {"file": page, "f_cnt":f_cnt, "cnt":f_cnt, 'page': page, 'paginator': paginator, 'dis_range': dis_range})


# 添加文件
def file_add(request, id):
    title = request.POST.get('name')
    file = request.FILES.get('inputfile')
    if file:
        basedir = os.path.abspath(os.path.join(os.path.dirname("__file__")))
        file_path = os.path.join(basedir, 'static', 'files', file.name)
        f = open(file_path, 'wb+')
        for chunk in file.chunks():
            f.write(chunk)
        f.close()
        genealogy = Genealogy.objects.get(id=id)
        file_item = File(filename=title, path=file.name, Genealogy=genealogy)
        file_item.save()

    return redirect('/genealogy/dtl_pdf/' + id)


# 删除文件：是一个请求，删除之后直接返回当前家谱的文件首页页面
def file_del(request, gid, id):
    File.objects.filter(id=id).update(is_del='1')
    return redirect('/genealogy/dtl_pdf/' + gid)


# 更新文件：分为get和post，get定位到update的文件编号；post之后直接返回当前家谱的文件首页页面
def file_upd(request):
    return render(request, 'genealogy/file_upd.html')


# 查看详细的文件：查看某个文件的详细信息页面，
def file_dtl(request):
    return render(request, 'genealogy/file_dtl.html')

#在给定族谱内查找文件
def file_search(request,id):
    g = Genealogy.objects.get(id=id)
    name = request.GET.get('name')
    cnt = File.objects.filter(Genealogy=g.title,is_del='0').count()
    f = File.objects.filter(Genealogy=g.title,filename__contains=name,is_del='0')
    f_cnt = f.count()
    page,paginator,dis_range = split_page(request,f)
    return render(request, 'genealogy/gene_dtl_pdf.html', {"g":g, "gid": id, "file": page, "name":name, "f_cnt":f_cnt, "cnt":cnt, 'page': page, 'paginator': paginator, 'dis_range': dis_range})

#在所有文件中查找文件
def search_file(request):
    name = request.GET.get('name')
    cnt = File.objects.filter(is_del='0').count()
    f = File.objects.filter(filename__contains=name,is_del='0')
    f_cnt = f.count()
    page,paginator,dis_range = split_page(request,f)
    return render(request, 'genealogy/file.html', {"file": page, "f_cnt":f_cnt, "cnt":cnt, 'page': page, "name":name, 'paginator': paginator, 'dis_range': dis_range})


# 文件下载，需要检查权限
def file_dwn(request, id):
    f = File.objects.get(id=id)
    basedir = os.path.abspath(os.path.join(os.path.dirname("__file__")))
    file_path = os.path.join(basedir, 'static', 'files', f.path)
    response = FileResponse(open(file_path, "rb"))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(f.path))
    return response

#文件预览
def file_view(request, id):
    f = File.objects.get(id=id)
    return render(request,'genealogy/file_dtl.html',{"f":f})

#=========================与指导说明相关的页面=========================
# 创建族谱指导说明页面
def guide_gene(request):
    return render(request, 'guide/gene.html')

def guide_indi(request):
    return render(request, 'guide/indi.html')

def guide_doc(request):
    return render(request, 'guide/doc.html')

# =========================与可视化相关的页面=========================
# 可视化首页
def vis(request):
    return render(request, 'vis/vis.html')
