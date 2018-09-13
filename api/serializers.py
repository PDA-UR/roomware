from rest_framework import serializers
from api.models import Snippet

class SnippetSerializer(serializers.Serializer):
	id = serializers.IntegerField(default=1)
	device = serializers.CharField(required=False, max_length=100, default='beamer')
	code = serializers.CharField(max_length=100)
	language = serializers.CharField(default='python', max_length=100)
	
	def create(self, validated_data):
		return Snippet().objects.create(**validated_data)
		
	#def update(self, instance, validated_data):
	#	instance.device = "beamer"
	#	instance.code = validated_data.get('code', instance.code)
	#	instance.language = "python"
	#	return instance
		
	
	#class Meta:
	#	model = Snippet
	#	fields = ('id', 'title', 'code', 'language')
