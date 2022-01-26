from django.urls import path
from django.urls import re_path
from . import views
from django.conf import settings 
from django.conf.urls.static import static 

from rest_framework.routers import DefaultRouter


urlpatterns= [
path("",views.search),
path("add",views.add_document),
path("delete",views.delete_document),
path("api/",views.myApiView.as_view()),
re_path(r'^api/(?P<pk>[0-9]+)$',views.myApiView.as_view()),
re_path(r'^api/(?P<pk>(.*?))$',views.myApiView.as_view()),

]