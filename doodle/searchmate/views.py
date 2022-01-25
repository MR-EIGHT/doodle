from django.shortcuts import render
from django_elasticsearch_dsl.documents import Document
from elasticsearch_dsl import document
from searchmate.documents import WebDocument
from typing import Text
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpRequest
from searchmate.models import webDoc
from elasticsearch_dsl import Q
# Create your views here.


def search(request):
    q=request.GET.get('q')
    if q:
        search = WebDocument.search()
        #search = search.sort('title','content')
        query = Q("multi_match", query=q, fields=['title', 'content'])
        docs = search.query(query)
        docs=docs[:10]
    else:
        docs = ''

    return render(request,"search.html",{'docs': docs})




def add_document(request):
    current = webDoc(
    title=request.GET['title'],
    content=request.GET['content'],
    url=request.GET['url'])
    current.save() #seve to db
    return HttpResponse(f"This Doc is saved successfully: {request.GET['title']} {request.GET['content']} {request.GET['url']}")


def delete_document(request):
    instance = webDoc.objects.get(id=request['id'])
    instance.delete()
    return HttpResponse(f"This Doc is deleted successfully: {id}")
