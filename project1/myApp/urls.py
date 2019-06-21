from django.conf.urls import url
from . import views  #引入当前目录下的views.py
urlpatterns = [
  url(r'^$',views.index),
  url(r'^all/$',views.allpage),
  url(r'^add/$',views.addpage),
  url(r'^addees/$', views.addees),
  url(r'^searche/$', views.search),
  url(r'^delete/(\d+)/$', views.delete),
  url(r'^update/$', views.update),
  url(r'^get/(\d+)/$', views.getid),
  url(r'^educe/$', views.educe),
]