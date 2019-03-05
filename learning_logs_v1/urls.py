#  定义learning_logs_v1的URL模式

from django.conf.urls import url
from . import views
# 这里对应的是learning_logs\urls中的namespaces
app_name = 'learning_logs_v1'
urlpatterns = [
    # 主页
    url(r'^$', views.index, name='index'),
    url(r'^topics/', views.topics, name='topics'),
    url(r'^topic_id/(?P<topic_id>\d+)/$', views.topic_id, name='topic_id'),
    url(r'^new_topic/$', views.new_topic, name='new_topic'),
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),
    url(r'^delete_entry/$', views.delete_entry, name='delete_entry'),
]
