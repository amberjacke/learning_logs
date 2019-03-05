from django.shortcuts import render,redirect
from .models import Topic,Entry
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .forms import TopicForm,EntryForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# 在这里写视图.
# 主页
def index(request):
    return render(request, 'learning_logs/index.html')


#  显示所有条目的主题
@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    # 生成paginator对象,定义每页显示3条记录
    paginator = Paginator(topics, 3)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)
    # 把当前的页码数转成整数类型
    currentPage = int(page)
    try:
        print(page)
        topics_list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        topics_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        topics_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    context = {'topics_list': topics_list, 'paginator': paginator}

    return render(request, 'learning_logs/topics.html', context)

#  显示单个主题和所有条目的主题
@login_required
def topic_id(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request, topic)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic_id.html', context)

#  添加新主题
@login_required
def new_topic(request):

    if request.method == 'GET':
        # 如果是GET请求，创建一个新表单
        form = TopicForm()
    if request.method == 'POST':
        # POST提交的数据，对数据进行处理
        form = TopicForm(request.POST)
        # 判断输入的是否有效
        if form.is_valid():
            # commit=False告诉Django先不提交到数据库.
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs_v1:topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

# 在特定的主题中添加新的条目
@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request, topic)
    if request.method == 'GET':
        form = EntryForm()
    # 对通过POST提交的表单进行处理
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            # 传递了实参
            new_entries = form.save(commit=False)
            new_entries.topic = topic
            new_entries.save()
            return HttpResponseRedirect(reverse('learning_logs_v1:topic_id', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

# 修改内容
@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request, topic)
    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            # 传递了参数
            form.save()
            return HttpResponseRedirect(reverse('learning_logs_v1:topic_id',args=[topic.id]))

    context = {'entry':entry,'topic':topic,'form':form}
    return render(request,'learning_logs/edit_entry.html',context)

#删除内容
@login_required
def delete_entry(request):
    entry_id = request.GET.get('id')
    Entry.objects.filter(id=entry_id).delete()
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def check_topic_owner(request, topic):
    if topic.owner != request.user:
        raise Http404