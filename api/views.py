from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from api.models import Snippet
from api.serializers import SnippetSerializer


# Create your views here.
@api_view(['GET', 'POST'])
def view_api(request):
	if request.method == 'GET':
		snippets = Snippet(code='print "hello, world"\n')
		serializer = SnippetSerializer(snippets)
		return JsonResponse(serializer.data, safe=False)
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = SnippetSerializer(data=request.data)
		if serializer.is_valid():
			return JSONResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

@api_view(['GET', 'POST'])		
def view_beamer(request):
	if request.method == 'GET':
		snippets = Snippet(device='beamer', code='changeState()')
		serializer = SnippetSerializer(snippets)
		return JsonResponse(serializer.data, safe=False)
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = SnippetSerializer(data=request.data)
		if serializer.is_valid():
			return JSONResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)
		
@api_view(['GET', 'POST'])		
def view_powerstrip(request):
	if request.method == 'GET':
		snippets = Snippet(device='powerstrip', code='switchOn(), switchOff()')
		serializer = SnippetSerializer(snippets)
		return JsonResponse(serializer.data, safe=False)
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = SnippetSerializer(data=request.data)
		if serializer.is_valid():
			return JSONResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

