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
from searchmate import preper

# Create your views here.

def correct(text):
    query = []

    spell_corrector = Corrector.Corrector()
    tokenizer = preper.Tokenizer()
    #spell_corrector.wspace_correction()
    #spell_corrector.sensitive_corrector()
    #spell_corrector.corrector()

    text=spell_corrector.wspace_correction(text)
    
    for word in tokenizer.tokenize(text):
        query.append(spell_corrector.corrector(word))

    return ' '.join(query)



def search(request):

    
    q=request.GET.get('q')

    if q:
        q = correct(q)

        search = WebDocument.search()
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
import json

class myApiView(APIView):
    serializers_class = serializers.DocsSerializer

    def get(self, request, pk=None, format=None):
    
        q=pk

        if q:

            q = correct(q)

            search = WebDocument.search()
            query = Q("multi_match", query=q, fields=['title', 'content'])
            docs = search.query(query)
            print(docs)
            docs=docs[:10]

            """
            jsonify
            """
            result= dict()
            i=0
            for item in docs:
                i+=1
                result[f'document {i}']={'title':item.title,'content':item.content,'url':item.url}
            docs = result
        else:
            docs = ''

        return Response(docs)



    def post(self, request):
        serializer = self.serializers_class(data=request.data)

        if serializer.is_valid():
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content')
            url = serializer.validated_data.get('url')


            normalizer = preper.Normalizer()
            tokenizer = preper.Tokenizer()


            new_doc = webDoc(

            title = normalizer.normalize(title),


            content = ' '.join(tokenizer.tokenize(normalizer.normalize(content))),


            url=url
            
            )

            new_doc.save()
            return Response({'message': f'New Doc is Saved!'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





    def put(self,request,pk):
        serializer = self.serializers_class(data=request.data)

        if serializer.is_valid():
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content')
            url = serializer.validated_data.get('url')
            webDoc.objects.filter(id=pk).update(title=title,content=content,url=url)
            return Response({'message': f'Doc ID: {pk} Updated!'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


 
    def patch(self,request,pk):
        serializer = self.serializers_class(data=request.data)

        if serializer.is_valid():
            title = serializer.validated_data.get('title',None)
            content = serializer.validated_data.get('content',None)
            url = serializer.validated_data.get('url',None)

            if title != None:
                webDoc.objects.filter(id=pk).update(title=title)

            if content != None:
                webDoc.objects.filter(id=pk).update(content=content)

            if url != None:
                webDoc.objects.filter(id=pk).update(url=url)



            return Response({'message': f'Doc ID: {pk} Patched!'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def delete(self,request,pk):
        instance = webDoc.objects.get(id=pk)
        instance.delete()
        return Response({'message': f'Doc ID: {id} Deleted!'})



        
"""
{
"title": "u",
"content":"test",
"url":"https://google.com"

}
"""