from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm

# 退出函数
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))

# 注册函数
def register(request):
    if request.method!='POST':
        # 显示空的表单
        form = UserCreationForm()
    else:
        # 处理填写好的表单
        form = UserCreationForm(data=request.POST)
        # 验证输入表单的数据是否合法
        if form.is_valid():
            new_user = form.save()
            #  让用户自动登陆，再重定向到主页
            authenticate_user = authenticate(username=new_user.username,password=request.POST['password1'])
            login(request,authenticate_user)
            return HttpResponseRedirect(reverse('learning_logs_v1:index'))

    context={'form':form}
    return render(request,'users/register.html',context)