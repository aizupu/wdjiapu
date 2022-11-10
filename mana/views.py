from math import e
from django.shortcuts import render, redirect
from home.views import genealogy
from mana.models import Role, Permission, UserInfo,Menu
from django.http import HttpResponse,JsonResponse
import datetime
from home.util import split_page, toJson
import re
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
# Create your views here.
def login(request):
    return render(request, 'home/login.html')

def logout(request):
    request.session['logged_in'] = False # 变成false 就意味着需要重新登录了
    del request.session[settings.SESSION_PERMISSION_URL_KEY]
    del request.session['user']
    del request.session['username']
    return render(request, 'home/index.html')

def login_submit(request):
    password = request.GET.get('password')
    username = request.GET.get('username')
    user = UserInfo.objects.filter(username=username, is_del=0)
    if len(user)==0:
        return HttpResponse("用户不存在")
    elif not check_password(password, user[0].password):
        return HttpResponse("密码错误")
    else:
        request.session['username']=user[0].nickname
        request.session['user']=toJson(user[0])
        request.session['logged_in']=True
        permissions=user[0].permissions.all()
        permission_url=set()
        reg = re.compile(r"'(.*?)'")
        for permission in permissions:
            permission_str=re.findall(reg, permission.url)
            permission_url.update(set(permission_str))
        request.session[settings.SESSION_PERMISSION_URL_KEY]=list(permission_url)
        request.session['role']=user[0].roles.all()[0].title
        response=HttpResponse(content="success", status=200)
        return response
    

def register(request):
    return render(request, 'home/register.html')
    
    
def register_submit(request):
    username = request.GET.get('username')
    user = UserInfo.objects.filter(username=username)
    if len(user)!=0:
        return render(request, 'home/login.html')
    password = request.GET.get('password')
    db_password = make_password(password, settings.PASSWORD_SECRET_KEY)
    gender = request.GET.get('gender')
    nickname = request.GET.get('nickname')
    email = request.GET.get('email')
    phone = request.GET.get('phone')
    add_time = datetime.datetime.now()
    title_str = request.GET.get('rtitle')
    role_title = Role.objects.filter(title=title_str)
    if len(role_title) == 0:
        role_item = Role(title=title_str)
        role_item.save()
    else:
        role_item = role_title[0]
    permission_str= request.GET.get('rpermission')
    permission_title = Permission.objects.filter(title=permission_str)
    if len(permission_title) == 0:
        menu_title = Menu.objects.filter(title="普通用户菜单")
        if len(menu_title)==0:
            menu_item = Menu(title="普通用户菜单")
            menu_item.save()
        else:
            menu_item=menu_title[0]
        permission_item = Permission(title=permission_str,menu=menu_item,url=settings.COMMON_USER_URL)
        print(permission_item.url)
        permission_item.save()
    else:
        permission_item = permission_title[0]
    user_item = UserInfo(username=username, password=db_password, gender=gender,nickname=nickname,
                         email=email,phone=phone,addtime=add_time)
    user_item.save()
    user_item.roles.set([role_item])
    user_item.permissions.set([permission_item])
    return HttpResponse("注册成功")
def upd_passwd(request):
    return render(request, 'home/upd_passwd.html')

def upd_passwd_submit(request):
    username = request.session['name']
    user = UserInfo.objects.filter(username=username)
    password = request.GET.get('password')
    if not check_password(password, user[0].password):
        return render(request,'home/upd_passwd.html',{"message":"密码错误","code":401})
    new_password = request.GET.get('new_password')
    new_password_check = request.GET.get('new_password_check')
    if new_password_check!=new_password:
        return render(request,'home/upd_passwd.html',{"message":"两次密码输入不一致","code":402})
    user.update(password=make_password(new_password, settings.PASSWORD_SECRET_KEY))
    return redirect('/genealogy')

def upd_userinfo(request):
    username = request.session['name']
    user = UserInfo.objects.get(username=username)
    return render(request, 'home/upd_userinfo.html',{'user':user})

def upd_userinfo_submit(request):
    username = request.session['name']
    user = UserInfo.objects.filter(username=username)
    nickname = request.GET.get('nickname')
    email = request.GET.get('email')
    phone = request.GET.get('phone')
    user.update(nickname=nickname,email=email,phone=phone)
    return redirect('/genealogy')


def user_list(request):
    u = UserInfo.objects.all().values()
    cnt = UserInfo.objects.filter(is_del='0').count()
    page,paginator,dis_range = split_page(request,u)
    return render(request, 'mana/user_list.html', {"user":page, "count": cnt,"u_cnt":cnt, 'page': page, 'paginator': paginator, 'dis_range': dis_range})


def u_add(request):
    return render(request, 'mana/user_add.html')


def user_add(request):
    username = request.GET.get('username')
    nickname = request.GET.get('nickname')
    phone = request.GET.get('phone')
    email = request.GET.get('email')
    role_type = int(request.GET.get('role'))
    print(role_type)
    if role_type==0:
        role_item=Role.objects.filter(title="研究人员")[0]
        permission_item=Permission.objects.filter(title="研究人员权限")[0]
    elif role_type==1:
        role_item=Role.objects.filter(title="普通用户")[0]
        permission_item=Permission.objects.filter(title="普通权限")[0]
    elif role_type==2:
        role_item=Role.objects.filter(title="管理员用户")[0]
        permission_item=Permission.objects.filter(title="管理员权限")[0]

    db_password=make_password(phone, settings.PASSWORD_SECRET_KEY)
    gender = int(request.GET.get('gender'))
    add_time = datetime.datetime.now()
    user_item = UserInfo(username=username, password=db_password, gender=gender,nickname=nickname,
                         email=email,phone=phone,addtime=add_time)
    user_item.save()
    print(role_item)
    user_item.roles.set([role_item])
    user_item.permissions.set([permission_item])
    return redirect('/user/list')

def user_del(request, id):
    UserInfo.objects.filter(id=id).update(is_del = '1')
    return redirect('/user/list')


def main(request):
    return render(request, 'mana/main.html')
