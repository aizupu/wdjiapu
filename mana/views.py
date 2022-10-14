from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'login.html')

def login_out(request):
    request.session['logged_in'] = False # 变成false 就意味着需要重新登录了
    return render("login.html")


def main(request):
    return render(request, 'mana/main.html')