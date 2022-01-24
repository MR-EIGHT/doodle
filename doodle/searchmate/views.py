from django.shortcuts import render
from django_elasticsearch_dsl.documents import Document
from elasticsearch_dsl import document
from searchmate.documents import WebDocument
from typing import Text
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpRequest
from searchmate.models import webDoc
# Create your views here.


def search(request):
    s = WebDocument.search().filter("term",title = 'urmia')
    
    for hit in s:
        print(hit.title)
        print(hit.content)
        print(hit.url)
    return render(request,"")




def add_document(request):
    current = webDoc(
    title=request.GET['title'],
    content=request.GET['content'],
    url=request.GET['url'])
    current.save() #seve to db
    return HttpResponse(f"This Doc is saved successfully: {request.GET['title']} {request.GET['content']} {request.GET['url']}")


def delete_document(request):
    instance = webDoc.objects.get(title=request.GET['title'],content=request.GET['content'],url=request.GET['url'])
    instance.delete()
    return HttpResponse(f"This Doc is saved successfully: {request.GET['title']} {request.GET['content']} {request.GET['url']}")
