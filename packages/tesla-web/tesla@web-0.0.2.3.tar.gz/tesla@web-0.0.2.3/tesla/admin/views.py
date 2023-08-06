
from tesla.auth.decorators import login_required
from tesla.auth.views import login as user_login
from tesla.response import HttpResponse, Redirect, Render, JsonResponse
from tesla.pyhtml import CT
from .models import User

from . import collections_manage

# your views


def collection(request):
    context = {}
    context['names'] = collections_manage.colls()
    print(context)
    return Render(request, 'admin/colls.html', context)

@login_required(path='admin/login')
def index(request):
    context = {}
    context['names'] = collections_manage.colls()
    print(context)
    return Render(request, 'admin/base_admin.html', context)


def login(request):
    
    if request.method == 'POST':
        u = request.post.get('username')
        p = request.post.get('password')
        print(u, p)
        user = User.get(username=u, password=p)
        if isinstance(user, User):
            user_login(request , user)
            return Redirect(request, '/admin')
    return Render(request, 'admin/login.html')



def register(request):
    if request.method == 'POST':
        u = request.post.get('username')
        e = request.post.get('email')
        p = request.post.get('password')
        user = User.create(username=u, email=e, password=p)
        user.save()
        print(user)
    return Render(request, 'admin/register.html')


def reset_password(request):
    if request.method == 'POST':
        print('es')
    return Render(request, 'admin/reset-password.html')


def logout(request):
    request.clear_cookie()
    return Redirect(request, 'admin:register')