from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns= [
path("",views.search),
path("add",views.add_document),
path("delete",views.delete_document),
path("api/",views.myApiView.as_view()),

]