from django.db import models
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json

# csrf https://stackoverflow.com/questions/22812721/why-do-i-get-csrf-cookie-not-set-when-post-to-django-rest-framework?rq=1 , last access 5.10.2018

class Snippet(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	classname = models.CharField(max_length=100)
	code = models.TextField()
	
	objects = models.Manager()
	
	class Meta:
		ordering = ('created',)

class SnippetSerializer(serializers.Serializer):
    classname = serializers.CharField(required=False, max_length=100)
    code = serializers.CharField(required=False, max_length=100)
	
    def create(self, validated_data):
        print("Hallo Welt", validated_data)
        return Snippet().objects.create(**validated_data)
        #return True
    
    def encode_api_json(self, data):
        classname = data['classname']
        code = data['code']
        print("api given class: ", classname, " given method: ", code)

    class Meta:
        model = Snippet
        fields = ('classname', 'code')

"""class PowerstripViewSet(APIView):

    @classmethod
    def get_extra_actions(cls):
        return []

    @api_view(['POST'])
    @csrf_exempt
    @action(methods=['post'], detail=True, url_path='on', url_name='on')
    def post(request,  *args, **kwargs):
        print("POST", request.data)
        data = list(request.POST)
        queryData = json.loads(str(data))
        print(queryData[0])
        name_class = queryData["name_class"]
        print(name_class)
        code = data[0][1]
        print("api given class: ", name_class, " given method: ", code)
        return Response("ok")
   
    @action(methods=['get'], detail=True, url_path='on', url_name='on')
    def powerstrip(self, request, pk=None):
        print("ViewSet, powerstrip")
        return Response("ok")"""
		
"""class PowerstripViewSet(ModelViewSet):
    #permission_classes = (permissions.AllowAny,)
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    print("POWERSTRIPVIEWSET")

    def post(self, request, format=None):
        print("POST", request.data)
        return Response("ok")

    @action(methods=['post'], detail=True, url_path='on', url_name='on')
    def powerstrip(self, request, pk=None):
        print("ViewSet, powerstrip")"""


