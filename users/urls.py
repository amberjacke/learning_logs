# 为应用程序users定义url模式

from django.conf.urls import url
from django.contrib.auth.views import login
from . import views
app_name = 'users'
urlpatterns = [
    # 登陆界面
    url(r'^login/$',login, {'template_name':'users/login.html'}, name='login'),
    # 退出
    url(r'^logout/$', views.logout_view, name='logout'),
    # 注册界面
    url(r'^register/$',views.register,name='register'),
]