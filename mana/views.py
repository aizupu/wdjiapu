from django.shortcuts import render, redirect
from mana.models import Role, Permission, UserInfo,Menu
from django.http import HttpResponse
# Create your views here.
def login(request):
    return render(request, 'home/login.html')

def logout(request):
    request.session['logged_in'] = False # 变成false 就意味着需要重新登录了
    return render(request, 'home/index.html')

def login_submit(request):
    password = request.GET.get('password')
    username = request.GET.get('username')
    user = UserInfo.objects.filter(username=username)
    if len(user)==0:
        return render(request, 'home/login.html',{"message":"用户不存在","code":400})
    elif password!=user[0].password:
        return render(request,'home/login.html',{"message":"密码错误","code":401})
    else:
        request.session['username']=user[0].nickname
        request.session['logged_in']=True
        print("登录成功")
        response=HttpResponse("success")
        response.set_cookie("logged_in",True)
        return response
    

def register(request):
    return render(request, 'home/register.html')
    
    
def register_submit(request):
    username = request.GET.get('username')
    user = UserInfo.objects.filter(username=username)
    if len(user)!=0:
        return render(request, 'home/login.html')
    password = request.GET.get('password')
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
        menu_title = Menu.objects.filter(title="默认菜单")
        if len(menu_title)==0:
            menu_item = Menu(title="默认菜单")
            menu_item.save()
        else:
            menu_item=menu_title[0]
        permission_item = Permission(title=permission_str,menu=menu_item,url=permission_str)
        permission_item.save()
    else:
        permission_item = permission_title[0]
    user_item = UserInfo(username=username, password=password, gender=gender,nickname=nickname,email=email,phone=phone,addtime=add_time)
    user_item.save()
    return render(request, 'home/login.html')


def main(request):
    return render(request, 'mana/main.html')