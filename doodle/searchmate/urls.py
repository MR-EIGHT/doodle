from django.urls import path
from . import views

urlpatterns= [
path("",views.search),
path("add",views.add_document),
path("delete",views.delete_document)

]