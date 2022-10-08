from django.shortcuts import render,redirect
from home.models import Genealogy
from home.models import Individual
import time
# Create your views here.

def index(request):
    return render(request, 'index2.html')

def login(request):
    return render(request, 'login.html')

def genealogy(request):
    g = Genealogy.objects.all().values()
    return render(request,"luru_genealogy.html",{"genealogy":g})

def genealogy_edit(request):
    genealogy_name = request.GET.get('genealogy_name')
    create_by = request.GET.get('create_by')
    genealogy_sername = request.GET.get('genealogy_sername')
    genealogy_location = request.GET.get('genealogy_location')
    hall_name = request.GET.get('hall_name')
    tag_name = request.GET.get('tag_name')
    now =  time.localtime()
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
    genealogy_item = Genealogy(title=genealogy_name,sername=genealogy_sername,hall_title=hall_name,county_title=tag_name,location=genealogy_location,create_time=now_time)
    genealogy_item.save()
    return redirect('/genealogy')

def genealogy_delete(request,id):
    g = Genealogy.objects.get(id=id)
    g.delete()
    return redirect('/genealogy')

def individual(request,id):
    p = Individual.objects.filter(gene_id = id).values
    return render(request,"luru_person.html",{"person":p,"gid":id})

def individual_add(request,id):
    return render(request,"luru_person1.html",{"gid":id})

def person_add(request,id):
    surname = request.GET.get('surname')
    common_name= request.GET.get('common_name')
    gender= request.GET.get('gender')
    father_id= request.GET.get('father_id')
    mother_id= request.GET.get('mother_id')
    prefix_name = request.GET.get('prefix_name')
    title_name = request.GET.get('title_name')
    line_name = request.GET.get('line_name')
    generation = request.GET.get('generation')
    rank = request.GET.get('rank')
    alive_flag = request.GET.get('alive_flag')
    ce_birth= request.GET.get('ce_birth')
    ce_death= request.GET.get('ce_death')
    birth_place= request.GET.get('birth_place')
    death_place= request.GET.get('death_place')
    biography= request.GET.get('biography')
    epitaph= request.GET.get('epitaph')
    genealogy = Genealogy.objects.get(id = id)
    # farther = Individual.objects.get(id = father_id)
    # mother = Individual.objects.get(id = mother_id)
    individual_item =  Individual(gene=genealogy, surname = surname, common_name = common_name, gender = gender, zi = prefix_name, hao = title_name,\
    line_name = line_name, generetion = generation, rank = rank, is_alive = alive_flag, ce_birth = ce_birth, ce_death = ce_death, birth_place = birth_place,\
    death_place = death_place, biography = biography, epitaph = epitaph)
    individual_item.save()
    return redirect('/individual/'+id)

def person_delete(request,gid,id):
    person = Individual.objects.get(id=id)
    person.delete()
    return redirect('/individual/'+gid)

def keshihua(request):
    g = Genealogy.objects.all().values()
    return render(request,"keshihua.html",{"genealogy":g})
