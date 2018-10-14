from rest_framework import serializers
from api.models import Snippet

class SnippetSerializer(serializers.Serializer):
    classname = serializers.CharField(required=True, max_length=100)
    code = serializers.CharField(max_length=100)
	
    def create(self, validated_data):
        return Snippet().objects.create(**validated_data)
    
    def encode_api_json(self, data):
        class_name = data['classname']
        code = data['code']
        print("serializer, api given class: ", class_name, " given method: ", code)
        return (class_name, code)

    class Meta:
        model = Snippet
        fields = ('classname', 'code')
