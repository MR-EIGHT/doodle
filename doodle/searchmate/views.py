from django.shortcuts import render
from searchmate.Document import WebDocument
from typing import Text
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpRequest
# Create your views here.


def search(request):
    s = WebDocument.search().filter("term",title = 'urmia')
    
    for hit in s:
        print(hit.title)
    return render(request,"")