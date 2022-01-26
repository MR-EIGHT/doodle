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
from .SpellingCorrector import Corrector

# Create your views here.

def correct(text):
    spell_corrector = Corrector()
    spell_corrector.wspace_correction()
    spell_corrector.sensitive_corrector()
    spell_corrector.corrector()




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




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from searchmate import serializers

class myApiView(APIView):
    serializers_class = serializers.mySerializer

    def get(self, request, format=None):

        return Response({'message':'Hello!'})

    def post(self, request):
        print(request.data)
        serializer = self.serializers_class(data=request.data)
        
        if serializer.is_valid():
            title = serializer.validated_data.get('title')
            message = f'Hello {title}'
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk=None):
        return Response({'message': 'put'})

    def patch(self,request,pk=None):
        return Response({'message': 'patch'})

    def delete(self,request,pk=None):
        return Response({'message': 'delete'})