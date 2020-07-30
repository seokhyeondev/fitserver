from django.conf.urls import url
from fitzme import views
 
urlpatterns = [
    url(r'^api/hotkeyword/$', views.hotkeyword_list),
    url(r'^api/searchlog/$', views.searchlog_list),
    url(r'^api/searchlog/(?P<email>[\w.@+-]+)/$', views.searchlog_list_detail),
    url(r'^api/feed/$', views.feed_list),
    url(r'^api/feed/(?P<pk>[0-9]+)/$', views.feed_list_detail)
]

