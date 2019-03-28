from django.views.generic import ListView, DetailView, View
from django.views.generic.base import ContextMixin
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from .models import *


class CommonMixin(ContextMixin, View):
    def get_context_data(self, **kwargs):
        # 判断请求是否携带登陆信息
        user = self.request.user
        if isinstance(user, AnonymousUser):
            username = None
        else:
            username = user.username

        kwargs.update({
            'username': username,
        })

        # 搜索
        query = self.request.GET.get('query', None)
        film_query = None
        if query:
            film_query = Film.objects.filter(name__contains=query)
        kwargs.update({
            'query': query,
            'film_query': film_query,
        })

        return super(CommonMixin, self).get_context_data(**kwargs)


class BaseFilmView(CommonMixin, ListView):
    model = Film
    template_name = 'html/index.html'

    def get_context_data(self, **kwargs):

        # 获取所有电影
        # film_list is [{label_1: film_1, label_2: film_2, ...}, {...}, ...]
        film_list = []
        index_label_all = IndexLabel.objects.all().order_by('id')  # 一级标签
        for index_label in index_label_all:
            film_map = {}
            for label in index_label.label.all():  # 二级标签
                film_map.update({label.name: label.film.all()})  # 获取电影数据
            film_list.append(film_map)

        return super(BaseFilmView, self).get_context_data(film_list=film_list)


class FilmPlayView(CommonMixin, DetailView):
    model = Film
    template_name = 'html/play.html'
    context_object_name = 'film'

    # 相当于@login_required修饰器，设置访问权限，没有携带登陆信息就跳到登陆页面
    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super(FilmPlayView, cls).as_view(*args, **kwargs)
        return login_required(view)


class RegisterView(View):
    context_data = {'alert': ''}

    def get(self, request):
        return render(request, 'html/register.html', self.context_data)

    def post(self, request):
        # 获取表单数据
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        # 查找是否存在重复名字，如果有提示警告
        if User.objects.filter(username=username).exists():
            self.context_data['alert'] = '已经存在该用户名，请重试'
        else:
            # 根据表单数据创建user
            user = User()
            user.username = username
            user.set_password(password)
            user.email = email
            user.save()
            # login
            login(request, user)
            # 定向回首页
            return redirect('index')

        return render(request, 'html/register.html', self.context_data)


class LoginView(View):
    context_data = {'alert': ''}

    def get(self, request):
        return render(request, 'html/register.html', self.context_data)

    def post(self, request):
        # 获取表单信息
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)  # 验证username和password是否对应得上
        if user is not None:
            # 通过验证登陆
            login(request, user)

            return redirect(reverse('index'))
        else:
            # 登陆失败
            self.context_data['alert'] = '用户名或密码错误'

        return render(request, 'html/register.html', self.context_data)


# 注销
def logout_view(request):
    logout(request)
    return redirect(reverse('index'))
